# daily-summary

Generate a summary of your commit history for the day.

## Usage:
export OPENAI_API_KEY=your-api-key

daily-summary --repo relative/path/to/your/repo --author "Author Name" --model <model-name>

--model is an optional argument that specifies the OpenAI model to be used. Defaults to "gpt-4" if not provided.
--date is optional but lets you create reports for different dates than today
  
  "Author Name" should match your git commit author name

## Publishing:

To publish a new version of the package, simply run the following command:
```
python3 publish.py
```
This script updates the package version, builds the package, and publishes it to PyPi using the credentials set in your environment variables.