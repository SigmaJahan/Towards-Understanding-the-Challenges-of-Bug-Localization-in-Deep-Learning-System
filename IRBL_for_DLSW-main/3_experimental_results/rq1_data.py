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


if os.path.exists("./results_rq1.txt") is False:

    path_dict = loader()

    base_path = path_dict["query_path"]
    files_path = path_dict["file_path"]
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
                gtfs = get_gtf(gtfs_path+repo+"\\"+ver+"\\"+bug+".txt")
                if len(gtfs) == 0:
                    continue
                print(repo, ver, bug)
                
                score_path = irbl_path+repo+"\\"+ver+"\\"+bug+"\\"
                file_scores = get_file_score(score_path+"sf_sim\\python_vsm.txt", norm)
                top_rank, rr, ap, _, _  = evaluation(file_scores, gtfs, len(file_scores), 100000) 
                f = open("./results_rq1.txt","a", encoding="utf8")
                f.write(repo+"\t"+ver+"\t"+bug+"\tvsm\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
                f.close()

                file_scores = get_file_score(score_path+"sf_sim\\python_rvsm.txt", norm)
                top_rank, rr, ap, _, _  = evaluation(file_scores, gtfs, len(file_scores), 100000) 
                f = open("./results_rq1.txt","a", encoding="utf8")
                f.write(repo+"\t"+ver+"\t"+bug+"\trvsm\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
                f.close()


                file_scores = get_file_score(score_path+"sf_sim\\python_bm25.txt", norm)
                top_rank, rr, ap, _, _  = evaluation(file_scores, gtfs, len(file_scores), 100000) 
                f = open("./results_rq1.txt","a", encoding="utf8")
                f.write(repo+"\t"+ver+"\t"+bug+"\tbm25\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
                f.close()
                                        

