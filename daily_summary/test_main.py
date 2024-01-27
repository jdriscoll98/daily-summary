import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from daily_summary.main import (daily_summary, extract_git_data,
                                get_local_git_author, summarize_all_diffs,
                                summarize_diff)


class TestMainFunctions(unittest.TestCase):

    @patch('git.Repo')
    def test_extract_git_data(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = [
            Mock(hexsha='abc123', authored_datetime=datetime(2023, 4, 1), author=Mock(name='John Doe'), message='Initial commit'),
            Mock(hexsha='def456', authored_datetime=datetime(2023, 4, 2), author=Mock(name='John Doe'), message='Added new feature'),
        ]
        mock_repo.return_value.branches = [Mock(name='main')]
        diffs = extract_git_data('.', 'John Doe', '2023-04-02')
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]['commit_hash'], 'def456')

    @patch('git.Repo')
    def test_get_local_git_author(self, mock_repo):
        mock_config_reader = Mock()
        mock_config_reader.get_value.return_value = 'John Doe'
        mock_repo.return_value.config_reader.return_value = mock_config_reader
        author_name = get_local_git_author('.')
        self.assertEqual(author_name, 'John Doe')

    @patch('openai.OpenAI.chat.completions.create')
    def test_summarize_diff(self, mock_completions_create):
        mock_completions_create.return_value.choices = [Mock(message=Mock(content='Summary of changes'))]
        summary = summarize_diff('diff --git a/file b/file')
        self.assertEqual(summary, 'Summary of changes')

    @patch('daily_summary.main.summarize_diff', return_value='Summary of changes')
    def test_summarize_all_diffs(self, mock_summarize_diff):
        diffs = [
            {"diff": "diff --git a/file b/file", "commit_hash": "abc123", "branch": "main", "date": "2023-04-02", "message": "Initial commit"},
        ]
        summaries = summarize_all_diffs(diffs, 'gpt-4')
        self.assertIn('Summary of changes', summaries)

    @patch('openai.OpenAI.chat.completions.create')
    def test_daily_summary(self, mock_completions_create):
        mock_completions_create.return_value.choices = [Mock(message=Mock(content='Your day in review'))]
        report = daily_summary('Summaries content', 'John Doe', '2023-04-02')
        self.assertEqual(report, 'Your day in review')

if __name__ == '__main__':
    unittest.main()
