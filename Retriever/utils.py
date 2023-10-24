from platform import release
import sys
import os
sys.path.insert(1, os.getcwd())
from Helper.helper_pygithub import *
import csv

def get_commit_code_fromGH(Rcsvpath = 'Project_link.csv', code_path = "Demo", release= "Demo"):
    '''
    This function is used to get the commit code from github. 
    The names of the files, states of the files before/after commit, hunk number, line number, names of the called functions, word number can be useful for the future.
    '''
    g, backup_keys, no_bused_key, accesskey = initialize_G()

    with open(Rcsvpath,"rU") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"', dialect=csv.excel_tab)
        data_read = [row for row in reader]
        load_object = 0
        
        for idx, line in enumerate(data_read):

            # commit_ids = line[-1].split("::")
            # commit_ids = [ids for ids in commit_ids if ids]
            repository = line[0].replace('https://api.github.com/repos/', '')
            user_name, repo_name = repository.split("/")
            pull_request_id = line[1]
            try:
                repo = g.get_repo(repository)
            except Exception as e:
                print("Repo not found")
                print(e)
                continue
            g, no_bused_key, load_object = changeG(g, accesskey, backup_keys, no_bused_key, load_object)
            if load_object:
                repo = g.get_repo(repository)
                print("New G loaded")
                load_object = 0
             
            merge_commit = repo.get_pull(int(pull_request_id)).merge_commit_sha
            if type(merge_commit) is list:
                merge_commit = merge_commit[0]


            try:
                commit = repo.get_commit(sha=merge_commit)
                for file_id, changes in enumerate(commit.files):
                    if changes.patch is not None:
                        if changes.filename.split(".")[-1] in ["py"]:
                            file_name = changes.filename.split("/")[-1]
                            if not os.path.exists(code_path+"/Codes/"+user_name+"::"+repo_name+"/"+release+"/"+pull_request_id+"/"+merge_commit+"/"+file_name):
                                os.makedirs(code_path+"/Codes/"+user_name+"::"+repo_name+"/"+release+"/"+pull_request_id+"/"+merge_commit+"/"+file_name)   
                            with open(code_path+"/Codes/"+user_name+"::"+repo_name+"/"+release+"/"+pull_request_id+"/"+merge_commit+"/"+file_name+"/old.py", "w") as fp1:
                                old_contents = repo.get_contents(changes.filename, ref=commit.parents[0].sha).decoded_content.decode()
                                fp1.write(old_contents)
                            with open(code_path+"/Codes/"+user_name+"::"+repo_name+"/"+release+"/"+pull_request_id+"/"+merge_commit+"/"+file_name+"/new.py", "w") as fp2:
                                new_contents = repo.get_contents(changes.filename, ref=commit.sha).decoded_content.decode()
                                fp2.write(new_contents)
                        else:
                            continue            
                    else:
                        continue                        
            except Exception as e:
                print("Commit not found")
                print(e)
                continue 
                   
get_commit_code_fromGH('Data/EcoSystem/python/python-docs-es/backport.csv',
 'data_code_stable')

# get_commit_code_fromGH('projectWise_data_from_github/CPython/stable-3.9.csv',
#  'data_code_stable', release="stable-3.9")

def get_allkinds_pull_requests_fromGHWithCLI(prjectlist = 'p_list.csv', output_file='complete', output_file_W_L ='complete_WL', output_file_wo_L ='complete_WOL', output_file_backport = 'complete_backport', output_file_cherry = 'complete_cherry_pick', output_file_normal='complete_normal'):
    file_path = 'Data/test/Candidate.csv'
    
    g, backup_keys, no_bused_key, accesskey = initialize_G()
 

    with open(file_path,"rU") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"', dialect=csv.excel_tab)
        data_read = [row for row in reader]
        data_read_write = []
        data_write_without_label = []
        data_read_write_with_Label = []
        data_read_write_with_backport = []
        data_read_write_with_cherry = []
        data_read_write_with_normalPR = []
        load_object = 0

        for idx, line in enumerate(data_read):
            repository = line[0].replace('https://api.github.com/repos/', '')
            user_name, repo_name = repository.split("/")
            print("Working on repo", repo_name)
            g, no_bused_key, load_object = changeG(g, accesskey, backup_keys, no_bused_key, load_object)
            if load_object:
                repo = g.get_repo(repository)
                print("New G loaded")
                load_object = 0
            try:
                repo = g.get_repo(repository)
                pulls = repo.get_pulls(state="closed")
            except Exception as e:
                print("Repo or pulls not found")
                print(e)
                continue
            
            
            pull_count = 0
            total_pulls = pulls.totalCount
            print(total_pulls)
            for x in range(1, 1000):
                try:
                    pull = pulls[x]

                    # if pull_count>5 : break
                    print("Working on pull", str(pull.number), "- Pull count:", pull_count)
                    pull_info = ''
                    pull_info_wL = ''
                    pull_info_wo_L = ''
                    review_comments = pull.get_comments()
                    # normal_comments = pull.get_issue_comments()
                    all_comments = ''
                    for review_comment in review_comments:
                        strp_comment = review_comment.body       
                        all_comments = all_comments + strp_comment + "::"
                    body = pull.body if pull.body is not None else '' 
                    pr_discussion = body + "::" + all_comments
                    pr_discussion = ' '.join([lineC.strip() for lineC in pr_discussion.strip().splitlines() if lineC.strip()])

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

                    pull_info = [line[0], str(pull.number), pull.head.ref+"::"+pull.base.ref, str(intra_branch), pr_status, pr_labels, pr_discussion, pull.user.name, pull.user.id, pull.user.followers, pull.commits, pull.additions, pull.deletions, pull.changed_files, len(pull.assignees), all_commits]
                    data_read_write.append(pull_info)
                    if 'backport' in pull.title.lower() or 'backport' in pr_labels.lower() or 'backport' in  pr_discussion.lower(): 
                        data_read_write_with_Label.append(pull_info)
                        if 'backport' in pull.title.lower() or 'backport' in pr_labels.lower():
                            data_read_write_with_backport.append(pull_info)
                        else:
                            data_write_without_label.append(pull_info)
                    if 'cherry' in pull.title.lower() or 'cherry' in pr_labels.lower() or 'cherry' in  pr_discussion.lower(): 
                        data_read_write_with_cherry.append(pull_info)
                    else:
                        data_read_write_with_normalPR.append(pull_info)                                   
                    pull_count = pull_count + 1 
                except Exception as e:
                    print("Problem in pulls")
                    # if hasattr(e, 'status') and getattr(e, 'status') == 403:
                    #     try:
                    #         g, no_bused_key, load_object = changeG(g, accesskey, backup_keys, no_bused_key, load_object)
                    #         if load_object:
                    #             repo = g.get_repo(repository)
                    #             print("New G loaded")
                    #             load_object = 0
                    #     except Exception as e1:
                    #         print(e1)
                    print(e)
                    continue

    with open(output_file, "wt") as fp1:
        writer = csv.writer(fp1, delimiter=",")
        writer.writerows(data_read_write)

    with open(output_file_W_L, "wt") as fp2:
        writerWL = csv.writer(fp2, delimiter=",")
        writerWL.writerows(data_read_write_with_Label)        

    with open(output_file_wo_L, "wt") as fp3:
        writerWo = csv.writer(fp3, delimiter=",")
        writerWo.writerows(data_write_without_label)

    with open(output_file_backport, "wt") as fp4:
        writerbackport = csv.writer(fp4, delimiter=",")
        writerbackport.writerows(data_read_write_with_backport)
    
    with open(output_file_cherry, "wt") as fp5:
        writernormal = csv.writer(fp5, delimiter=",")
        writernormal.writerows(data_read_write_with_cherry)

    with open(output_file_normal, "wt") as fp6:
        writernormal = csv.writer(fp6, delimiter=",")
        writernormal.writerows(data_read_write_with_normalPR)

# get_allkinds_pull_requests_fromGHWithCLI('Candidate.csv', 
# 'cpython_all_PRs.csv', 
# 'cpython_keywordsPRs.csv',
# 'cpython_in_Discussion_OnlyPRs.csv', 
# 'cpython_backport_in_TitleandLabes_PRs.csv',
# 'cpython_cherry_in_keyword_Discussion_TitleandLabel.csv' 
# 'cpython_normal_PRs.csv')