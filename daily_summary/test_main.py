import unittest
from unittest.mock import Mock, patch

from daily_summary.main import (daily_summary, extract_git_data, generate,
                                get_local_git_author, git, summarize_all_diffs,
                                summarize_diff)


class TestMainFunctions(unittest.TestCase):

    @patch('daily_summary.main.git.Repo')
    def test_extract_git_data(self, mock_repo):
        # Setup mock objects and return values
        mock_repo.return_value.iter_commits.return_value = [Mock(hexsha='abc123', authored_datetime=Mock(date=Mock(strftime=lambda x: '2023-04-01')), author=Mock(name='Test Author'), message='Test commit message')]
        mock_repo.return_value.branches = [Mock(name='main')]
        mock_repo.return_value.git.diff.return_value = 'diff --git a/file b/file'

        # Test successful extraction
        diffs = extract_git_data('.', 'Test Author', '2023-04-01')
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]['branch'], 'main')
        self.assertEqual(diffs[0]['commit_hash'], 'abc123')
        self.assertEqual(diffs[0]['author'], 'Test Author')
        self.assertEqual(diffs[0]['date'], '2023-04-01 00:00:00')
        self.assertEqual(diffs[0]['message'], 'Test commit message')
        self.assertEqual(diffs[0]['diff'], 'diff --git a/file b/file')

        # Test with no author provided and no commits found
        mock_repo.return_value.iter_commits.return_value = []
        diffs = extract_git_data('.', None, '2023-04-01')
        self.assertEqual(diffs, [])

        # Test with no commits on the specified date
        mock_repo.return_value.iter_commits.return_value = [Mock(authored_datetime=Mock(date=Mock(strftime=lambda x: '2023-04-02')))]
        diffs = extract_git_data('.', 'Test Author', '2023-04-01')
        self.assertEqual(diffs, [])

    @patch('daily_summary.main.git.Repo')
    def test_get_local_git_author(self, mock_repo):
        # Setup mock objects and return values
        mock_config_reader = Mock()
        mock_config_reader.get_value.return_value = 'Test Author'
        mock_repo.return_value.config_reader.return_value = mock_config_reader

        # Test successful retrieval of author name
        author_name = get_local_git_author('.')
        self.assertEqual(author_name, 'Test Author')

        # Test failure to retrieve author name
        mock_repo.side_effect = git.exc.InvalidGitRepositoryError
        author_name = get_local_git_author('.')
        self.assertIsNone(author_name)

    @patch('daily_summary.main.client.chat.completions.create')
    def test_summarize_diff(self, mock_completions_create):
        # Setup mock objects and return values
        mock_response = Mock(choices=[Mock(message=Mock(content='Summary of changes'))])
        mock_completions_create.return_value = mock_response

        # Test successful summarization
        summary = summarize_diff('diff --git a/file b/file')
        self.assertEqual(summary, 'Summary of changes')

    @patch('daily_summary.main.summarize_diff')
    def test_summarize_all_diffs(self, mock_summarize_diff):
        # Setup mock objects and return values
        mock_summarize_diff.return_value = 'Summary of changes'
        diffs = [
            {
                'branch': 'main',
                'commit_hash': 'abc123',
                'author': 'Test Author',
                'date': '2023-04-01 00:00:00',
                'message': 'Test commit message',
                'diff': 'diff --git a/file b/file'
            }
        ]

        # Test successful summarization of all diffs
        summaries = summarize_all_diffs(diffs, 'gpt-4')
        self.assertIn('1. Commit: abc123', summaries)
        self.assertIn('Summary of changes', summaries)

    @patch('daily_summary.main.client.chat.completions.create')
    def test_daily_summary(self, mock_completions_create):
        # Setup mock objects and return values
        mock_response = Mock(choices=[Mock(message=Mock(content='Your day in review'))])
        mock_completions_create.return_value = mock_response

        # Test successful creation of daily summary
        summary = daily_summary('Summaries', 'Test Author', '2023-04-01')
        self.assertEqual(summary, 'Your day in review')

    @patch('daily_summary.main.daily_summary')
    def test_generate(self, mock_daily_summary):
        # Setup mock objects and return values
        mock_daily_summary.return_value = 'Your day in review'

        # Test successful generation of report
        report = generate('Summaries', 'Test Author', '2023-04-01', 'gpt-4')
        self.assertEqual(report, 'Your day in review')

if __name__ == '__main__':
    unittest.main()
