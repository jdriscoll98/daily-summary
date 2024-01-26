# daily-summary

Generate a summary of your commit history for the day.

Usage:
export OPENAI_API_KEY=your-api-key
daily-summary --repo relative/path/to/your/repo --author "Author Name" --model <model-name>

--model is an optional argument that specifies the OpenAI model to be used. Defaults to "gpt-4" if not provided.

"Author Name" should match your git commit author name

TODO: 

High priority: 
1. Add --date arg to create a report for any date
2. use all branches instead of just current one
3. Author should be inferred from local git configuration if not provided as an arg

Other:

1. Error handling
2. Date windows (--start_date, --end_date ?)