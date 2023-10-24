from github import Github
from platform import release
import sys
import os
sys.path.insert(1, os.getcwd())
from Helper.helper_pygithub import *
import csv

g, backup_keys, no_bused_key, accesskey = initialize_G()
repository_names =[ 
"python/buildmaster-config",
"python/python-docs-es",
"python/peps",
"python/miss-islington",
"python/core-workflow",
"python/cpython",
"python/mypy",
"python/docsbuild-scripts",
"python/bedevere",
"python/typeshed",
"python/cherry-picker",
"python/devguide",
"python/typing_extensions",
"python/importlib_metadata",
"python/typing",
"python/python-docs-fr",
"python/typed_ast"
]

repository_names_eclipse = [
"eclipse/buildship",
"eclipse/jkube",
"eclipse/wakaama",
"eclipse/amlen",
"eclipse/lsp4e",
"eclipse/microprofile-graphql",
"eclipse/xtext",
"eclipse/mosquitto",
"eclipse/paho.mqtt.c",
"eclipse/swtchart",
"eclipse/kiso-testing",
"eclipse/paho.mqtt-sn.embedded-c",
"eclipse/paho.mqtt.python",
"eclipse/xtext-core",
"eclipse/xtext-maven",
"eclipse/xtext-xtend",
"eclipse/xtext-extras",
"eclipse/sommr",
"eclipse/january",
"eclipse/che",
"eclipse/jetty.project",
"eclipse/kapua",
"eclipse/kura",
"eclipse/eclipse-collections",
"eclipse/kitalpha",
"eclipse/microprofile-metrics",
"eclipse/microprofile-config",
"eclipse/tm4e",
"eclipse/eclipsefuro-web",
"eclipse/capella",
"eclipse/microprofile-rest-client",
"eclipse/microprofile-open-api",
"eclipse/microprofile-fault-tolerance",
"eclipse/capella-xhtml-docgen",
"eclipse/xtext-eclipse"
]


data_read_write = []

for repository_name in repository_names:
    # Get the repository
    try:
        repo = g.get_repo(repository_name)

        releases = repo.get_releases()
        loc = repo.get_languages().get('Python', 0)  # Assuming you're interested in Python LOC
        commits = repo.get_commits()
        issues = repo.get_issues(state='all')
        releases = repo.get_releases()
        contributors = repo.get_contributors()
        num_contributors = len(list(contributors))

        repo_info = [repository_name, loc, commits.totalCount, issues.totalCount ,num_contributors]
        data_read_write.append(repo_info)

        print(f"Repository: {repository_name}")
        # print(f"Latest Release Version: {latest_release}")
        print(f"Lines of Code (LOC): {loc}")
        print(f"Number of Commits: {commits.totalCount}")
        print(f"Number of Issues: {issues.totalCount}")
        print("=" * 30)

    except Exception as e:
        print(e)

with open("repo.csv", "wt") as fp1:
    writer = csv.writer(fp1, delimiter=",")
    writer.writerows(data_read_write)