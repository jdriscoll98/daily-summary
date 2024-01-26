import git

# Replace with your repository's path
repo_path = '../mxlocker-web'
repo = git.Repo(repo_path)

first_commit = list(repo.iter_commits())[-1].hexsha

for commit in repo.iter_commits():
    print('Commit:', commit.hexsha)
    print('Author:', commit.author.name)
    print('Date:', commit.authored_datetime)
    print('Message:', commit.message.strip())

    # Check if it's the first commit
    if commit.hexsha != first_commit:
        print('Diff:', repo.git.diff(commit.hexsha + '^', commit.hexsha))
    else:
        print('Diff: First commit in the repository')

    print('-' * 40)
