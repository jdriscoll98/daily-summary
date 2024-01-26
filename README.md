# daily-summary

Generate a summary of your commit history for the day.

Usage:
export OPENAI_API_KEY=your-api-key
daily-summary --repo relative/path/to/your/repo --author "Author Name" [--date DATE]

"Author Name" should match your git commit author name
--date is optional but lets you create reports for different dates than today