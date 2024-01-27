import unittest
from datetime import datetime
from unittest.mock import Mock, patch

import main


class TestMain(unittest.TestCase):

    @patch('main.git.Repo')
    def test_extract_git_data_with_author_and_date(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = [
            Mock(hexsha='abc123', authored_datetime=datetime(2023, 4, 1), author=Mock(name='John Doe'), message='Initial commit'),
            Mock(hexsha='def456', authored_datetime=datetime(2023, 4, 2), author=Mock(name='John Doe'), message='Added new feature'),
        ]
        mock_repo.return_value.branches = [Mock(name='main'), Mock(name='feature')]
        mock_repo.return_value.git.diff.return_value = 'diff --git a/file b/file'
        diffs = main.extract_git_data('.', 'John Doe', '2023-04-02')
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]['commit_hash'], 'def456')
        self.assertEqual(diffs[0]['author'], 'John Doe')
        self.assertEqual(diffs[0]['message'], 'Added new feature')

    @patch('main.git.Repo')
    def test_extract_git_data_without_author(self, mock_repo):
        mock_repo.return_value.config_reader.return_value.get_value.return_value = 'Jane Smith'
        mock_repo.return_value.iter_commits.return_value = []
        diffs = main.extract_git_data('.', None, '2023-04-02')
        self.assertEqual(diffs, [])

    @patch('main.git.Repo')
    def test_get_local_git_author_success(self, mock_repo):
        mock_repo.return_value.config_reader.return_value.get_value.return_value = 'Jane Smith'
        author_name = main.get_local_git_author('.')
        self.assertEqual(author_name, 'Jane Smith')

    @patch('main.git.Repo')
    def test_get_local_git_author_failure(self, mock_repo):
        mock_repo.side_effect = Exception('Error')
        author_name = main.get_local_git_author('.')
        self.assertIsNone(author_name)

    @patch('main.client.chat.completions.create')
    def test_summarize_diff(self, mock_completions):
        mock_completions.return_value.choices[0].message.content = 'Summary of changes'
        summary = main.summarize_diff('diff --git a/file b/file')
        self.assertEqual(summary, 'Summary of changes')

    @patch('main.client.chat.completions.create')
    def test_summarize_all_diffs(self, mock_completions):
        mock_completions.return_value.choices[0].message.content = 'Summary of changes'
        diffs = [{'diff': 'diff --git a/file b/file', 'commit_hash': 'abc123', 'branch': 'main', 'date': '2023-04-02', 'message': 'Added new feature'}]
        summaries = main.summarize_all_diffs(diffs, 'gpt-4')
        self.assertIn('Summary of changes', summaries)

    @patch('main.client.chat.completions.create')
    def test_daily_summary(self, mock_completions):
        mock_completions.return_value.choices[0].message.content = 'Your day in review'
        summaries = '1. Commit: abc123\n   Branch: main\n   Date: 2023-04-02\n   Message: Added new feature\n   Key Changes: Summary of changes\n'
        report = main.daily_summary(summaries, 'John Doe', '2023-04-02')
        self.assertEqual(report, 'Your day in review')

    @patch('main.daily_summary')
    def test_generate(self, mock_daily_summary):
        mock_daily_summary.return_value = 'Generated report'
        summaries = 'Summaries of diffs'
        report = main.generate(summaries, 'John Doe', '2023-04-02', 'gpt-4')
        self.assertEqual(report, 'Generated report')

    @patch('main.argparse.ArgumentParser')
    @patch('main.sys.exit')
    @patch('main.extract_git_data')
    @patch('main.summarize_all_diffs')
    @patch('main.generate')
    def test_main_integration(self, mock_generate, mock_summarize_all_diffs, mock_extract_git_data, mock_exit, mock_argparse):
        mock_argparse.return_value.parse_args.return_value = Mock(repo='.', author='John Doe', date='2023-04-02', model='gpt-4')
        mock_extract_git_data.return_value = []
        mock_summarize_all_diffs.return_value = 'Summaries of diffs'
        mock_generate.return_value = 'Generated report'
        main.main()
        mock_generate.assert_called_once_with('Summaries of diffs', 'John Doe', '2023-04-02', 'gpt-4')

if __name__ == '__main__':
    unittest.main()
