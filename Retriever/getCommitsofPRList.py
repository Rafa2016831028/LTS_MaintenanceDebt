from github import Github
from platform import release
import sys
import os
sys.path.insert(1, os.getcwd())
from Helper.helper_pygithub import *
import csv

# Replace these with your own credentials


pull_request_ids =[209,206]
    
data_read_write = []
data_read_write_with_Label =[]
url ="https://api.github.com/repos/apache/sedona"

# Initialize a Github instance
g, backup_keys, no_bused_key, accesskey = initialize_G()

# Get the repository
repo = g.get_repo("apache/sedona")


def get_pull_request(pull_request_id):
    pull_request = repo.get_pull(pull_request_id)
    return pull_request

for pull_request_id in pull_request_ids:
    try:
        pull = get_pull_request(pull_request_id)
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
        if 'backport' in pull.title.lower() or 'backport' in pr_labels.lower() or 'backport' in pull.body.lower(): 
            data_read_write_with_Label.append(pull_info)

    except Exception as e:
        print(e)

with open("backport.csv", "wt") as fp1:
    writer = csv.writer(fp1, delimiter=",")
    writer.writerows(data_read_write)