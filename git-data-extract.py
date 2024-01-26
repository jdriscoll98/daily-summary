import git
from datetime import datetime
import json
# Replace with your repository's path
repo_path = '/path/to/your/repo'
repo = git.Repo(repo_path)

today = datetime.now().date()

first_commit = list(repo.iter_commits())[-1].hexsha

diffs = []
for commit in repo.iter_commits():
    commit_date = commit.authored_datetime.date()

    if commit_date == today and commit.author.name == 'Jack Driscoll':
        diff_data = {
            'commit_hash': commit.hexsha,
            'author': commit.author.name,
            'date': str(commit.authored_datetime),
            'message': commit.message.strip(),
            'diff': repo.git.diff(commit.hexsha + '^', commit.hexsha) if first_commit != commit.hexsha else 'First Commit'
        }
        diffs.append(diff_data)

# Writing diffs to a file
with open('diffs.json', 'w') as file:
    json.dump(diffs, file, indent=4)
