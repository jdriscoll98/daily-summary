import argparse
from datetime import datetime
from .generate_daily_summary import generate
from .summarize_diff import summarize_all_diffs
from .git_data_extract import extract_git_data
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Generate daily development reports.")
    if os.environ.get("OPENAI_API_KEY") is None:
        sys.stderr.write(
            "Error: OPENAI_API_KEY environment variable is not set. Please set the variable and try again.\n"
        )
        sys.exit(1)
    parser.add_argument(
        "--repo",
        help="Path to the repository to generate the report for",
        required=True,
    )
    parser.add_argument(
        "--author",
        help="Name of the author to generate the report for",
        required=True,
    )

    parser.add_argument(
        "--date",
        help="Date for the report in YYYY-MM-DD format",
        default=datetime.now().date().strftime("%Y-%m-%d"),
    )
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="OpenAI model to be used for generating summaries",
    )
    args = parser.parse_args()
    print("Generating daily development report...")
    print("Extracting git data...")
    extract_git_data(args.repo, args.author, args.date)  # Pass date to extract_git_data
    print("Summarizing diffs...")
    summarize_all_diffs(args.model)
    print("Generating daily summary...")
    generate(args.date, args.model)  # Pass date to generate
    # clean up the diffs.json file and summaries.txt file
    os.remove("diffs.json")
    os.remove("summaries.txt")
    print("Done!")


if __name__ == "__main__":
    main()
