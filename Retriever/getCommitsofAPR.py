from github import Github
from platform import release
import sys
import os
sys.path.insert(1, os.getcwd())
from Helper.helper_pygithub import *
import csv

# Replace these with your own credentials

pull_request_number = 233  # Replace with the actual pull request number


data_read_write = []

url ="https://api.github.com/repos/eclipse/capella-xhtml-docgen"

# Initialize a Github instance
g, backup_keys, no_bused_key, accesskey = initialize_G()

# Get the repository
repo = g.get_repo("eclipse/capella-xhtml-docgen")

# Get the pull request
pull = repo.get_pull(pull_request_number)

intra_branch = 0
if (pull.head.label.split(':')[0]==pull.base.label.split(':')[0]):     
    intra_branch = 1
    pr_status = 'closed'    
if pull.merged:
    pr_status = 'merged'
pr_labels = ''    
for label in pull.labels:
    pr_labels = pr_labels + label.name+'::'

all_commits = ''

for commit in pull.get_commits():
    all_commits = all_commits + commit.sha + "::"

pull_info = [url, str(pull.number), pull.head.ref+"::"+pull.base.ref, str(intra_branch), pr_status, pr_labels, pull.user.name, pull.user.id, pull.user.followers, pull.commits, pull.additions, pull.deletions, pull.changed_files, len(pull.assignees), all_commits]
data_read_write.append(pull_info)

with open("capella-xhtml-docgen_backport.csv", "wt") as fp1:
    writer = csv.writer(fp1, delimiter=",")
    writer.writerows(data_read_write)