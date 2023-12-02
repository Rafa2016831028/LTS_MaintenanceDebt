# from github import Github

# # Initialize a Github instance
# g = Github()

# # List of repositories
# repos = [
#     "eclipse/buildship",
#     "eclipse/jkube",
#     "eclipse/wakaama",
#     # Add more repositories as needed
# ]

# # Loop through repositories
# for repo_name in repos:
#     # Get the repository object
#     repo = g.get_repo(repo_name)

#     # Get the latest commit
#     latest_commit = repo.get_commits()[0]

#     # Print information about the commit
#     print(f"Repository: {repo_name}")
#     print(f"Commit SHA: {latest_commit.sha}")
#     print(f"Commit Message: {latest_commit.commit.message}")
#     print(f"Author: {latest_commit.commit.author.name}")
#     print(f"Date: {latest_commit.commit.author.date}\n")

import uuid

commit_ids = [str(uuid.uuid4()) for _ in range(385)]

# Print the list of commit IDs
for commit_id in commit_ids:
    print(commit_id)