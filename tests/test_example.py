import unittest
from unittest import mock
from daily_summary.main import extract_git_data


class TestExample(unittest.TestCase):

    def test_extract_git_data_ignores_different_dates(self):
        with mock.patch('git.Repo') as mock_repo:
            # Create mock commits with different dates and same authors
            mock_commit_different_date = mock.Mock()
            mock_commit_different_date.hexsha = 'abc1234'
            mock_commit_different_date.authored_datetime = mock.Mock()
            mock_commit_different_date.authored_datetime.date.return_value = mock.Mock()
            mock_commit_different_date.authored_datetime.date.return_value.strftime.return_value = '2022-01-01'
            mock_commit_different_date.author.name = 'John Doe'

            mock_commit_same_date = mock.Mock()
            mock_commit_same_date.hexsha = 'def5678'
            mock_commit_same_date.authored_datetime = mock.Mock()
            mock_commit_same_date.authored_datetime.date.return_value = mock.Mock()
            mock_commit_same_date.authored_datetime.date.return_value.strftime.return_value = '2023-01-01'
            mock_commit_same_date.author.name = 'John Doe'

            # Mock iter_commits method to return commits
            mock_repo.iter_commits.return_value = [mock_commit_different_date, mock_commit_same_date]

            # Call the extract_git_data with mock data
            diffs = extract_git_data('/fake/repo_path', 'John Doe', '2023-01-01')

            # Assert that diffs do not contain commit with a different date
            self.assertNotIn(mock_commit_different_date.hexsha, [diff['commit_hash'] for diff in diffs])

            # Assert that diffs only contain commits with the same date
            self.assertIn(mock_commit_same_date.hexsha, [diff['commit_hash'] for diff in diffs])
        self.assertEqual(1, 0)
