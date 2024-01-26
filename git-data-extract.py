import git

# Replace with your repository's path
repo_path = '.'
repo = git.Repo(repo_path)

for commit in repo.iter_commits():
    print('Commit:', commit.hexsha)
    print('Author:', commit.author.name)
    print('Date:', commit.authored_datetime)
    print('Message:', commit.message)
    print('Diff:', repo.git.diff(commit.hexsha, commit.hexsha + '^'))
    print('-' * 40)
