from openai import OpenAI
import json
import os
from tqdm import tqdm

# Get the API key from the environment variable
client = OpenAI()
client.api_key = os.environ['OPENAI_API_KEY']

def summarize_diff(diff): 
    response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
        "role": "system",
        "content": "Summarize the key changes in this code diff. Don't say \" the key changes are this\" just say the key changes."
        },
        {
        "role": "user",
        "content": diff,
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content

def summarize_all_diffs(diffs):
    # Summarize the diffs
    summaries = ''
    for i, diff_data in tqdm(enumerate(diffs, start=1)):
        diff_summary = summarize_diff(diff_data['diff'])
        summary_file += (f"{i}. Commit: {diff_data['commit_hash']}\n")
        summary_file += (f"   Date: {diff_data['date']}\n")
        summary_file += (f"   Message: {diff_data['message']}\n")
        summary_file += (f"   Key Changes: {diff_summary}\n")
        summary_file += ('-' * 40 + '\n')
    return summaries