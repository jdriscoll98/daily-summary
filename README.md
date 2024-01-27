# daily-summary

Generate a summary of your commit history for the day.

## Usage:
export OPENAI_API_KEY=your-api-key

daily-summary --repo relative/path/to/your/repo --author "Author Name" --model <model-name>

--model is an optional argument that specifies the OpenAI model to be used. Defaults to "gpt-4" if not provided.
--date is optional but lets you create reports for different dates than today
  
  "Author Name" should match your git commit author name

## Publishing:

To publish a new version to PyPi, run the automation script:
`./scripts/publish.py <new_version>`

Note: Ensure you have the necessary permissions to upload to PyPI and that the PYPI_TOKEN environment variable is set.