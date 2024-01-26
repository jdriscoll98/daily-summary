# daily-summary

Generate a summary of your commit history for the day.

Usage:
export OPENAI_API_KEY=your-api-key
daily-summary --repo relative/path/to/your/repo --author "Author Name" --model <model-name>

--model is an optional argument that specifies the OpenAI model to be used. Defaults to "gpt-4" if not provided.

"Author Name" should match your git commit author name
