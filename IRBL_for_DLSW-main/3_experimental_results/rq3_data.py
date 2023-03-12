import os
import numpy
import random

def get_gtf(gtf_path):
    gtf_lines = open(gtf_path, "r", encoding="utf8").readlines()
    gtf_list = []
    for line in gtf_lines:
        line = line.replace("\n","")
        if len(line) > 3:
            gtf_list.append(line)
    return gtf_list

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

path_dict = loader()

base_path = path_dict["query_path"]
files_path = path_dict["file_path"]
gtfs_path = path_dict["gtf_path"]
irbl_path = path_dict["irbl_path"]

if os.path.exists("./results_rq3.txt") is False:
    norm = True
    k_days = [0, 1, 2, 3, 4] 
    k_days_value = [15, 30, 60, 90, 150]
    weight_list = numpy.arange(0, 1.05, 0.1)
    repos = os.listdir(base_path)
    loc_bug_num = 0
    all_bugs = 0
    weights_mrr ={}
    weights_map ={}
    weights_bugnum ={}               
    for repo in repos:
        vers = os.listdir(base_path+repo+"\\")
        for ver in vers:
            bugs = os.listdir(base_path+repo+"\\"+ver+"\\")
            for bug in bugs:
                if os.path.exists(gtfs_path+repo+"\\"+ver+"\\"+bug+".txt") is False:
                    continue            
                gtfs = get_gtf(gtfs_path+repo+"\\"+ver+"\\"+bug+".txt")
                if len(gtfs) == 0:
                    continue
                print(repo, ver, bug)

                score_path = irbl_path+repo+"\\"+ver+"\\"+bug+"\\"

                br_scores = get_bug_sim(score_path+"br_sim\\bm25.txt", norm)
                commit_scores = get_commit_score(score_path+"commit_score\\score.txt", norm)
                strace_scores = get_strace_score(score_path+"strace_sim\\strace_score.txt", norm)
                hunks_scores = get_hunk_score(score_path+"commit_score\\bm25_hunk_sim.txt", norm)
                file_scores = get_file_score(score_path+"sf_sim\\python_bm25.txt", norm)

                file_numbers = len(file_scores)
                print(repo, ver, bug, len(gtfs), len(br_scores), len(commit_scores), len(strace_scores), len(hunks_scores), len(file_scores))
                for alpha in list(weight_list): # BR sim
                    for beta in list(weight_list):  # commit sim
                        for gamma in list(weight_list): # stract sim
                            for dalta in list(weight_list): # hunk sim
                                for zeta in list(weight_list):  # file sim
                                    if (alpha+beta+gamma+dalta+zeta) < 0.99:
                                        continue
                                    if (alpha+beta+gamma+dalta+zeta) > 1.01:
                                        continue
                                    weights = [alpha, beta, gamma, dalta, zeta]
                                    weights_str = [str(round(w,1)) for w in weights] 
                                    for k_day in k_days:
                                        integrated_scores = merge_score(br_scores, commit_scores, strace_scores, hunks_scores, file_scores, weights, k_day)
                                        if random.random() > 0.999:                                       
                                            print('\t'.join(weights_str), str(k_days_value[k_day]), repo, ver, bug, len(gtfs), top_rank, round(rr,3), round(ap,3), sep="\t")
                                        top_rank, rr, ap, _, _  = evaluation(integrated_scores, gtfs, file_numbers, 100000) 

                                        f = open("./results_rq3.txt", "a", encoding="utf8")
                                        f.write('\t'.join(weights_str)+"\t"+str(k_days_value[k_day])+"\t"+repo+"\t"+ver+"\t"+bug+"\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
                                        f.close()
                                        label = '-'.join(weights_str)+"-"+str(k_days_value[k_day])
                                        if label not in weights_mrr.keys():
                                            weights_mrr[label] = 0
                                            weights_map[label] = 0
                                            weights_bugnum[label] = 0
                                        weights_mrr[label] += rr
                                        weights_map[label] += ap
                                        weights_bugnum[label] += 1
                loc_bug_num += 1
    print(loc_bug_num, all_bugs)


    sim_scores_sort = sorted(weights_mrr.items(), reverse=True, key=lambda item: item[1])
    ind = 0
    for key, _ in sim_scores_sort:
        bug_num = weights_bugnum[key]
        rr = weights_mrr[key]
        ap = weights_map[key]
        print(key, rr/bug_num, ap/bug_num)
        ind += 1
        if ind == 10:
            break