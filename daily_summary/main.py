import argparse
from .generate_daily_summary import generate
from .summarize_diff import summarize_all_diffs
from .git_data_extract import extract_git_data
import os


def main():
    parser = argparse.ArgumentParser(description="Generate daily development reports.")
    parser.add_argument(
        "--repo",
        help="Path to the repository to generate the report for",
        required=False,
    )
    parser.add_argument(
        "--author",
        help="Name of the author to generate the report for",
        required=False,
    )
    # Add arguments as needed. For example:
    # parser.add_argument('--date', help='Date for the report', required=True)
    parser.add_argument(
        "--infer-author",
        help="Infer the author name from the local git configuration",
        action='store_true',
        required=False
    )

    args = parser.parse_args()
    print("Generating daily development report...")
    print("Extracting git data...")
    diffs = extract_git_data(args.repo, args.author if args.author is not None else None, args.infer_author)  # Example usage
    print("Summarizing diffs...")
    summaries = summarize_all_diffs(diffs)
    print("Generating daily summary...")
    generate(summaries)
    print("Done!")
