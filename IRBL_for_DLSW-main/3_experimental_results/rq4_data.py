import os
import numpy
import random
        

def get_bug_sim(br_sim_path, norm):
    bug_sim_dict = {}
    max_score = 0
    min_score = 9999999
    if os.path.exists(br_sim_path) is False:
        return bug_sim_dict
    
    lines = open(br_sim_path,"r", encoding="utf8")
    for line in lines:
        line = line.replace("\n","")
        if line.find("\t") == -1:
            continue
        file_id = line.split("\t")[0]
        score = float(line.split("\t")[1])
        if max_score < score:
            max_score = score
        if min_score > score:
            min_score = score
        bug_sim_dict[file_id] = score
    
    if norm is True:
        norm_bug_sim_dict = {}
        for id in bug_sim_dict.keys():
            score = bug_sim_dict[id]        
            if max_score >  min_score:
                score = (score - min_score) / (max_score - min_score)
            elif max_score == min_score:
                score = 1
            else:
                print("error!!")
            norm_bug_sim_dict[id] = score
        return norm_bug_sim_dict
    else:
        return bug_sim_dict

def get_commit_score(commit_path, norm):
    commit_score_dict = {}
    max_score = 0
    min_score = 9999999
    if os.path.exists(commit_path) is False:
        return commit_score_dict
    
    lines = open(commit_path,"r", encoding="utf8")
    for line in lines:
        line = line.replace("\n","")
        if line.find("\t") == -1:
            continue
        file_id = line.split("\t")[0]     
        score_list = []
        for score in line.split("\t")[1:]:
            if len(score) < 1:
                continue
            score = float(score)
            score_list.append(score)
            if max_score < score:
                max_score = score
            if min_score > score:
                min_score = score
        commit_score_dict[file_id] = score_list
    
    if norm is True:
        norm_commit_score_dict = {}
        for id in commit_score_dict.keys():
            score_list = commit_score_dict[id]        
            norm_score_list = []
            for score in score_list:
                if max_score >  min_score:
                    score = (score - min_score) / (max_score - min_score)
                elif max_score == min_score:
                    score = 1
                else:
                    print("error!!")
                norm_score_list.append(score)
            norm_commit_score_dict[id] = norm_score_list
        return norm_commit_score_dict
    else:
        return commit_score_dict

def get_strace_score(strace_path, norm):
    strace_score_dict = {}
    max_score = 0
    min_score = 9999999
    if os.path.exists(strace_path) is False:
        return strace_score_dict
    lines = open(strace_path,"r", encoding="utf8").readlines()
    for line in lines:
        line = line.replace("\n","")
        if line.find("\t") == -1:
            continue
        file_id = line.split("\t")[0]
        score = float(line.split("\t")[1])
        if max_score < score:
            max_score = score
        if min_score > score:
            min_score = score
        strace_score_dict[file_id] = score

    if norm is True:
        norm_strace_score_dict = {}
        for id in strace_score_dict.keys():
            score = strace_score_dict[id]        
            if max_score >  min_score:
                score = (score - min_score) / (max_score - min_score)
            elif max_score == min_score:
                score = 1
            else:
                print("error!!")
            norm_strace_score_dict[id] = score
        return norm_strace_score_dict
    else:
        return strace_score_dict
        
def get_file_score(file_path, norm):
    file_sim_dict = {}
    max_score = 0
    min_score = 9999999
    
    lines = open(file_path,"r", encoding="utf8").readlines()
    for line in lines:
        line = line.replace("\n","")
        file_id = line.split("\t")[0]
        score = float(line.split("\t")[1])
        if max_score < score:
            max_score = score
        if min_score > score:
            min_score = score
        file_sim_dict[file_id] = score
    
    if norm is True:
        norm_file_sim_dict = {}
        for id in file_sim_dict.keys():
            score = file_sim_dict[id]           
            if max_score >  min_score:
                score = (score - min_score) / (max_score - min_score)
            elif max_score == min_score:
                score = 1
            else:
                print("error!!")
            norm_file_sim_dict[id] = score
        return norm_file_sim_dict
    else:
        return file_sim_dict

def get_hunk_score(hunk_path, norm):
    hunk_score_dict = {}
    if os.path.exists(hunk_path) is False:
        return hunk_score_dict
    
    lines = open(hunk_path,"r", encoding="utf8")
    max_score = 0
    min_score = 9999999
    for line in lines:
        line = line.replace("\n","")
        if line.find("\t") == -1:
            continue
        file_id = line.split("\t")[0]
        score_list = []
        for score in line.split("\t")[1:]:
            if len(score) < 1:
                continue
            score = float(score)
            if max_score < score:
                max_score = score
            if min_score > score:
                min_score = score
            score_list.append(score)
        hunk_score_dict[file_id] = score_list[0]
    
    if norm is True:
        norm_hunk_score_dict = {}
        for id in hunk_score_dict.keys():
            score = hunk_score_dict[id]          
            if max_score >  min_score:
                score = (score - min_score) / (max_score - min_score)
            elif max_score == min_score:
                score = 1
            else:
                print("error!!")
            norm_hunk_score_dict[id] = score
        return norm_hunk_score_dict
    else:
        return hunk_score_dict

def merge_score(br_scores, commit_scores, strace_scores, hunks_scores, file_scores, weights, k_day):
    integrated_scores = {}
    for file_id in file_scores.keys():        
        br_score = 0
        if file_id in br_scores.keys():
            br_score = br_scores[file_id]
        commit_score = 0
        if file_id in commit_scores.keys():
            commit_score = commit_scores[file_id][k_day]
        strace_score = 0
        if file_id in strace_scores.keys():
            strace_score = strace_scores[file_id]
        hunk_score = 0
        if file_id in hunks_scores.keys():
            hunk_score = hunks_scores[file_id]

        file_score = file_scores[file_id]
        score = br_score * weights[0] + commit_score * weights[1] + strace_score * weights[2] + hunk_score * weights[3] + file_score * weights[4]
        integrated_scores[file_id] = score
    return integrated_scores
   

def get_gtf(gtf_path):
    gtf_list = []
    if os.path.exists(gtf_path) is False:
        return gtf_list
    gtf_lines = open(gtf_path, "r", encoding="utf8").readlines()    
    for line in gtf_lines:
        line = line.replace("\n","")
        if len(line) > 3:
            gtf_list.append(line)
    return gtf_list

def evaluation(sim_scores, gtf_list, files_num, num_top_index):
    sim_scores_sort = sorted(sim_scores.items(), reverse=True, key=lambda item: item[1])
    rank = 1
    top_rank = files_num
    rr = 0
    ap = 0
    find_bug_num = 0
    non_buggy_file_indexes = []
    top_file_indexes = []
    for key, _ in sim_scores_sort:
        if len(gtf_list) == find_bug_num and len(top_file_indexes) == num_top_index:
            break
        if key in gtf_list:
            find_bug_num += 1
            if rr == 0:
                rr = 1.0 / rank
                top_rank = rank
            ap += find_bug_num / rank
        if len(non_buggy_file_indexes) < 10:
            non_buggy_file_indexes.append(key)
        if rank < num_top_index:
            top_file_indexes.append(key)
        rank += 1
    if find_bug_num > 0:
        ap = ap / find_bug_num
    return top_rank, rr, ap, non_buggy_file_indexes, top_file_indexes

def loader():
    path_dict = {}
    lines = open("./z_config.txt","r", encoding="utf8").readlines()
    for line in lines:
        line = line.replace("\n","")
        tokens = line.split("=",2)
        label = tokens[0]
        path = tokens[1]
        path_dict[label] = path
    return path_dict


k_days = [0, 1, 2, 3, 4] 
k_days_value = [15, 30, 60, 90, 150]

weights= [0.0, 0.2, 0.4, 0.2, 0.2]
k_day =2 # 60
path_dict = loader()
base_path = path_dict["query_path"]
files_path = path_dict["file_path"]
functions_path = path_dict["function_path"]
gtfs_path = path_dict["gtf_path"]
irbl_path = path_dict["irbl_path"]

norm = True
loc_bug_num = 0
all_bugs = 0
weights_mrr ={}
weights_map ={}
weights_bugnum ={}  
repos = os.listdir(base_path)             
for repo in repos:
    vers = os.listdir(base_path+repo+"\\")
    for ver in vers:
        bugs = os.listdir(base_path+repo+"\\"+ver+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+ver+"\\"+bug+".txt") is False:
                continue            
            gtfs = get_gtf(gtfs_path+repo+"\\"+ver+"\\"+bug+"_method.txt")
            if len(gtfs) == 0:
                continue
            
            mth_file_key_dict = {}
            lines = open(functions_path+repo+"\\"+ver+"\\pythonKeyMap.txt","r", encoding="utf8").readlines()
            for line in lines:
                tokens = line.split("|")
                file_id = tokens[0]
                mth_id = tokens[2]
                mth_file_key_dict["python-"+mth_id] = "python-"+file_id

            print(repo, ver, bug)            
            
            score_path = irbl_path+repo+"\\"+ver+"\\"+bug+"\\"

            mth_sim_scores = get_file_score(score_path+"mth_sim\\python_bm25.txt", norm)
            top_rank, rr, ap, _, _  = evaluation(mth_sim_scores, gtfs, len(mth_sim_scores), 100000) 
            print(repo, bug, rr, ap)            
            f = open("./results_rq4.txt","a", encoding="utf8")
            f.write(repo+"\t"+ver+"\t"+bug+"\tM\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
            f.close()
            if "M" not in weights_mrr.keys():
                weights_mrr["M"] = 0
                weights_map["M"] = 0
                weights_bugnum["M"] = 0

                weights_mrr["FM"] = 0
                weights_map["FM"] = 0
                weights_bugnum["FM"] = 0

                weights_mrr["BLM"] = 0
                weights_map["BLM"] = 0
                weights_bugnum["BLM"] = 0
            
            weights_mrr["M"] += rr
            weights_map["M"] += ap
            weights_bugnum["M"] += 1
            
            file_sim_scores = get_file_score(score_path+"sf_sim\\python_bm25.txt", norm)
            mth_file_sim_scores = {}
            for key in mth_sim_scores.keys():
                mth_score = mth_sim_scores[key]
                file_id = mth_file_key_dict[key]
                file_score = file_sim_scores[file_id]                
                mth_file_sim_scores[key] = file_score + mth_score
            top_rank, rr, ap, _, _  = evaluation(mth_file_sim_scores, gtfs, len(mth_file_sim_scores), 100000) 
            print(repo, bug, rr, ap)
            f = open("./results_rq4.txt","a", encoding="utf8")
            f.write(repo+"\t"+ver+"\t"+bug+"\tF+M\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
            f.close()
            
            weights_mrr["FM"] += rr
            weights_map["FM"] += ap
            weights_bugnum["FM"] += 1
            

            br_scores = get_bug_sim(score_path+"br_sim\\bm25.txt", norm)
            commit_scores = get_commit_score(score_path+"commit_score\\score.txt", norm)
            strace_scores = get_strace_score(score_path+"strace_sim\\strace_score.txt", norm)
            hunks_scores = get_hunk_score(score_path+"commit_score\\bm25_hunk_sim.txt", norm)
            file_scores = get_file_score(score_path+"sf_sim\\python_bm25.txt", norm)
            integrated_scores = merge_score(br_scores, commit_scores, strace_scores, hunks_scores, file_scores, weights, k_day)
                                    
            mth_file_sim_scores = {}
            for key in mth_sim_scores.keys():                
                mth_score = mth_sim_scores[key]
                file_id = mth_file_key_dict[key]
                file_score = integrated_scores[file_id]
                mth_file_sim_scores[key] = file_score + mth_score
            top_rank, rr, ap, _, _  = evaluation(mth_file_sim_scores, gtfs, len(mth_file_sim_scores), 100000) 
            print(repo, bug, rr, ap)
            f = open("./results_rq4.txt","a", encoding="utf8")
            f.write(repo+"\t"+ver+"\t"+bug+"\tBL+M\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
            f.close()
            
            
            weights_mrr["BLM"] += rr
            weights_map["BLM"] += ap
            weights_bugnum["BLM"] += 1


for key in weights_bugnum.keys():
    print(key, weights_bugnum[key], round(weights_mrr[key]/weights_bugnum[key],3),round(weights_map[key]/weights_bugnum[key],3))