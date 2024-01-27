import os
import sys
import unittest
from io import StringIO
from unittest.mock import mock_open, patch

from daily_summary.main import argparse, main


class TestMain(unittest.TestCase):

    @patch('sys.exit')
    def test_environment_variable(self, mock_exit):
        with patch.dict('os.environ', {}, clear=True):
            with patch('sys.stderr', new=StringIO()) as fake_err:
                main()
                self.assertIn("OPENAI_API_KEY environment variable is not set", fake_err.getvalue())
                mock_exit.assert_called_once_with(1)

    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parsing(self, mock_args):
        mock_args.return_value = argparse.Namespace(
            repo="test_repo",
            author="test_author",
            date="2023-04-01",
            model="gpt-4"
        )
        with patch('daily_summary.main.extract_git_data') as mock_extract:
            mock_extract.return_value = []
            with patch('sys.exit'):
                main()
                mock_args.assert_called()
                self.assertEqual(mock_args.return_value.repo, "test_repo")
                self.assertEqual(mock_args.return_value.author, "test_author")
                self.assertEqual(mock_args.return_value.date, "2023-04-01")
                self.assertEqual(mock_args.return_value.model, "gpt-4")

    @patch('daily_summary.main.extract_git_data', return_value=[])
    @patch('sys.exit')
    def test_no_diffs_behavior(self, mock_exit, mock_extract):
        with patch('argparse.ArgumentParser.parse_args'):
            main()
            mock_extract.assert_called()
            mock_exit.assert_called_once_with(0)

    @patch('daily_summary.main.summarize_diff', return_value="Summary of changes")
    def test_diff_summarization(self, mock_summarize):
        diffs = [{'diff': 'fake_diff_data'}]
        with patch('daily_summary.main.extract_git_data', return_value=diffs):
            with patch('argparse.ArgumentParser.parse_args'):
                main()
                mock_summarize.assert_called_once_with('fake_diff_data', 'gpt-4')

    @patch('daily_summary.main.daily_summary', return_value="Daily development report content")
    @patch('daily_summary.main.extract_git_data', return_value=[{'diff': 'fake_diff_data'}])
    @patch('daily_summary.main.summarize_all_diffs', return_value="Summarized diffs")
    def test_report_generation(self, mock_summarize_all, mock_extract, mock_daily_summary):
        with patch('argparse.ArgumentParser.parse_args'):
            with patch('builtins.open', mock_open()) as mocked_file:
                main()
                mocked_file.assert_called_once_with("daily_summary.md", "w")
                mocked_file().write.assert_called_once_with("Daily development report content")
                mock_daily_summary.assert_called_once_with("Summarized diffs", None, "2023-04-01", "gpt-4")

if __name__ == '__main__':
    unittest.main()
