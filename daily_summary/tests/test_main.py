import unittest
from unittest.mock import Mock, patch

import git
from daily_summary.main import (daily_summary, extract_git_data, generate,
                                get_local_git_author, summarize_all_diffs,
                                summarize_diff)
from openai import OpenAI


class TestExtractGitData(unittest.TestCase):
    @patch('git.Repo')
    def test_extract_git_data_valid(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = [
            Mock(hexsha='abc123', authored_datetime=Mock(date=Mock(strftime=lambda x: '2023-04-01')), author=Mock(name='Test Author'), message='Test commit message'),
            Mock(hexsha='def456', authored_datetime=Mock(date=Mock(strftime=lambda x: '2023-04-01')), author=Mock(name='Test Author'), message='Another commit message')
        ]
        mock_repo.return_value.branches = [Mock(name='main'), Mock(name='dev')]
        mock_repo.return_value.git.diff.return_value = 'diff --git a/file b/file'
        diffs = extract_git_data('.', 'Test Author', '2023-04-01')
        self.assertEqual(len(diffs), 2)
        self.assertEqual(diffs[0]['branch'], 'main')
        self.assertEqual(diffs[0]['commit_hash'], 'abc123')

    @patch('git.Repo')
    def test_extract_git_data_no_commits(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = []
        diffs = extract_git_data('.', 'Test Author', '2023-04-01')
        self.assertEqual(diffs, [])

    @patch('git.Repo')
    def test_extract_git_data_invalid_author(self, mock_repo):
        with self.assertRaises(SystemExit):
            extract_git_data('.', 'Invalid Author', '2023-04-01')

    @patch('git.Repo')
    def test_extract_git_data_invalid_date(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = [
            Mock(hexsha='abc123', authored_datetime=Mock(date=Mock(strftime=lambda x: '2023-04-02')), author=Mock(name='Test Author'), message='Test commit message')
        ]
        diffs = extract_git_data('.', 'Test Author', '2023-04-01')
        self.assertEqual(diffs, [])

class TestGetLocalGitAuthor(unittest.TestCase):
    @patch('git.Repo')
    def test_get_local_git_author_success(self, mock_repo):
        mock_config_reader = Mock()
        mock_config_reader.get_value.return_value = 'Test Author'
        mock_repo.return_value.config_reader.return_value = mock_config_reader
        author_name = get_local_git_author('.')
        self.assertEqual(author_name, 'Test Author')

    @patch('git.Repo', side_effect=git.exc.InvalidGitRepositoryError)
    def test_get_local_git_author_invalid_repo(self, mock_repo):
        author_name = get_local_git_author('.')
        self.assertIsNone(author_name)

class TestSummarizeDiff(unittest.TestCase):
    @patch.object(OpenAI, 'chat')
    def test_summarize_diff_valid(self, mock_chat):
        mock_chat.completions.create.return_value = Mock(choices=[Mock(message=Mock(content='Summary of changes'))])
        summary = summarize_diff('diff --git a/file b/file', 'gpt-4')
        self.assertEqual(summary, 'Summary of changes')

class TestSummarizeAllDiffs(unittest.TestCase):
    @patch('daily_summary.main.summarize_diff')
    def test_summarize_all_diffs_valid(self, mock_summarize_diff):
        mock_summarize_diff.return_value = 'Summary of changes'
        diffs = [
            {"branch": "main", "commit_hash": "abc123", "author": "Test Author", "date": "2023-04-01", "message": "Test commit message", "diff": "diff --git a/file b/file"},
            {"branch": "dev", "commit_hash": "def456", "author": "Test Author", "date": "2023-04-01", "message": "Another commit message", "diff": "diff --git a/file b/file"}
        ]
        summaries = summarize_all_diffs(diffs, 'gpt-4')
        self.assertIn('1. Commit: abc123', summaries)
        self.assertIn('Summary of changes', summaries)

    def test_summarize_all_diffs_empty(self):
        summaries = summarize_all_diffs([], 'gpt-4')
        self.assertEqual(summaries, '')

class TestDailySummary(unittest.TestCase):
    @patch.object(OpenAI, 'chat')
    def test_daily_summary_valid(self, mock_chat):
        mock_chat.completions.create.return_value = Mock(choices=[Mock(message=Mock(content='Your day in review'))])
        report = daily_summary('Summaries content', 'Test Author', '2023-04-01', 'gpt-4')
        self.assertEqual(report, 'Your day in review')

class TestGenerate(unittest.TestCase):
    @patch('daily_summary.main.daily_summary')
    def test_generate_valid(self, mock_daily_summary):
        mock_daily_summary.return_value = 'Your day in review'
        report = generate('Summaries content', 'Test Author', '2023-04-01', 'gpt-4')
        self.assertEqual(report, 'Your day in review')

if __name__ == '__main__':
    unittest.main()
