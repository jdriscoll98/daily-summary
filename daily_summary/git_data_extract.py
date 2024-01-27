import git
from datetime import datetime
import json
import logging


# Replace with your repository's path
def extract_git_data(repo_path, author, date):
    repo = git.Repo(repo_path)

    first_commit = list(repo.iter_commits())[-1].hexsha

    diffs = []
    author = author if author is not None else get_local_git_author(repo_path)
    if not author:
        logging.error("Author name could not be inferred from local git configuration and was not provided as an argument.")
        exit(1)


    for commit in repo.iter_commits():
        commit_date = commit.authored_datetime.date().strftime("%Y-%m-%d")
        if commit_date == date and commit.author.name == author:
            diff_data = {
                "commit_hash": commit.hexsha,
                "author": commit.author.name,
                "date": str(commit.authored_datetime),
                "message": commit.message.strip(),
                "diff": repo.git.diff(commit.hexsha + "^", commit.hexsha)
                if first_commit != commit.hexsha
                else "First Commit",
            }
            diffs.append(diff_data)

    return diffs

def get_local_git_author(repo_path):
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        config_reader = repo.config_reader()
        author_name = config_reader.get_value('user', 'name', None)
        return author_name
    except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError, git.exc.GitCommandError, KeyError):
        logging.error("Could not retrieve the author name from the local git configuration.")
        return None