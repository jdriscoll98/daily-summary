import unittest
from datetime import datetime
from unittest import mock

from daily_summary.main import (extract_git_data, generate, main,
                                summarize_all_diffs)


class TestMain(unittest.TestCase):

    @mock.patch('daily_summary.main.open', new_callable=mock.mock_open)
    @mock.patch('daily_summary.main.daily_summary')
    def test_generate(self, mock_daily_summary, mock_open):
        mock_daily_summary.return_value = "Mocked daily summary report"
        report = generate("summaries", "author", "2023-04-01", "gpt-4")
        mock_open.assert_called_once_with("daily_summary.md", "w")
        mock_open().write.assert_called_once_with("Mocked daily summary report")
        self.assertEqual(report, "Mocked daily summary report")

    @mock.patch('daily_summary.main.argparse.ArgumentParser.parse_args')
    @mock.patch('daily_summary.main.os.environ.get')
    @mock.patch('daily_summary.main.extract_git_data')
    @mock.patch('daily_summary.main.summarize_all_diffs')
    @mock.patch('daily_summary.main.generate')
    def test_main(self, mock_generate, mock_summarize_all_diffs, mock_extract_git_data, mock_environ_get, mock_parse_args):
        mock_environ_get.return_value = "mock_api_key"
        mock_parse_args.return_value = mock.Mock(repo=".", author="test_author", date="2023-04-01", model="gpt-4")
        mock_extract_git_data.return_value = ["diff1", "diff2"]
        mock_summarize_all_diffs.return_value = "summary"
        mock_generate.return_value = "report"

        with mock.patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_not_called()

        mock_environ_get.assert_called_once_with("OPENAI_API_KEY")
        mock_extract_git_data.assert_called_once_with(".", "test_author", "2023-04-01")
        mock_summarize_all_diffs.assert_called_once_with(["diff1", "diff2"], "gpt-4")
        mock_generate.assert_called_once_with("summary", "test_author", "2023-04-01", "gpt-4")

    @mock.patch('daily_summary.main.git.Repo')
    def test_extract_git_data(self, mock_repo):
        mock_repo.return_value.iter_commits.return_value = []
        diffs = extract_git_data(".", "author", "2023-04-01")
        self.assertEqual(diffs, [])

    @mock.patch('daily_summary.main.client.chat.completions.create')
    def test_summarize_all_diffs(self, mock_chat_completions_create):
        mock_chat_completions_create.return_value = mock.Mock(choices=[mock.Mock(message=mock.Mock(content="Mocked summary"))])
        diffs = [{"diff": "diff data", "commit_hash": "abc123", "branch": "main", "date": "2023-04-01", "message": "Commit message"}]
        summaries = summarize_all_diffs(diffs, "gpt-4")
        expected_summary = "1. Commit: abc123\n   Branch: main\n   Date: 2023-04-01\n   Message: Commit message\n   Key Changes: Mocked summary\n" + "-" * 40 + "\n"
        self.assertEqual(summaries, expected_summary)

if __name__ == '__main__':
    unittest.main()
