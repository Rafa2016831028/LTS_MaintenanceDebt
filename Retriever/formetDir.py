from github import Github
from platform import release
import sys
import os
sys.path.insert(1, os.getcwd())
from Helper.helper_pygithub import *
import csv
import random

# Replace 'YOUR_GITHUB_API_TOKEN' with your actual GitHub API token
g = g, backup_keys, no_bused_key, accesskey = initialize_G()

# List of repositories
repositories = [
    'eclipse/xtext-core',
    'eclipse/xtext-maven',
    'eclipse/xtext-xtend',
    'eclipse/microprofile-metrics',
    'eclipse/xtext-eclipse',
    'eclipse/jkube',
    'eclipse/tm4e',
    'eclipse/xtext',
    'eclipse/xtext-extras',
    'eclipse/paho.mqtt.python',
    'eclipse/microprofile-graphql',
    'eclipse/microprofile-config',
    'eclipse/microprofile-open-api',
    'eclipse/xtext-core',
    'eclipse/microprofile-graphql',
    'eclipse/microprofile-fault-tolerance',
    'eclipse/jetty.project',
    'eclipse/eclipse-collections',
    'eclipse/kapua',
    'eclipse/microprofile-open-api',
    'eclipse/xtext-eclipse',
    'eclipse/xtext-core',
    'eclipse/eclipse-collections',
    'eclipse/xtext-eclipse',
    'eclipse/jkube',
    'eclipse/xtext-core',
    'eclipse/microprofile-config',
    'eclipse/eclipse-collections',
    'eclipse/microprofile-fault-tolerance',
    'eclipse/eclipse-collections',
    'eclipse/xtext-extras',
    'eclipse/paho.mqtt.c',
    'eclipse/microprofile-rest-client',
    'eclipse/microprofile-metrics',
    'eclipse/microprofile-metrics',
    'eclipse/xtext-maven',
    'eclipse/xtext-maven',
    'eclipse/xtext-maven',
    'eclipse/xtext-maven',
    'eclipse/xtext-maven',
    'eclipse/microprofile-config',
    'eclipse/microprofile-metrics',
    'eclipse/xtext-xtend',
    'eclipse/microprofile-graphql',
    'eclipse/microprofile-config',
    'eclipse/microprofile-rest-client',
    'eclipse/paho.mqtt.c',
    'eclipse/xtext',
    'eclipse/microprofile-rest-client',
    'eclipse/jkube',
    'eclipse/xtext-core',
    'eclipse/paho.mqtt.c',
    'eclipse/microprofile-open-api',
    'eclipse/jetty.project',
    'eclipse/jetty.project',
    'eclipse/kapua',
    'eclipse/xtext-extras',
    'eclipse/xtext-xtend',
    'eclipse/xtext-xtend',
    'eclipse/xtext-core',
    'eclipse/eclipse-collections',
    'eclipse/microprofile-fault-tolerance'
]

def get_random_commit(repo):
    commits = repo.get_commits()
    random_commit = random.choice(list(commits))
    return random_commit

data=[]
for repo_name in repositories:
    try:
        repo = g.get_repo(repo_name)
        commit = get_random_commit(repo)
        data.append[commit]
    except Exception as e:
        print(f"Error fetching random commit in {repo_name}: {e}")

print("\n")

get_random_commit(repositories)

with open("capella-xhtml-docgen_backport.csv", "wt") as fp1:
    writer = csv.writer(fp1, delimiter=",")
    writer.writerows(data)