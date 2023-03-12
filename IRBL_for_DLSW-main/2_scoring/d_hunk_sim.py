import os
import time
import json
from dateutil.parser import parse as date_parser
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util

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
bugs_path = path_dict["bug_path"]
query_path = path_dict["query_path"]
files_path = path_dict["file_path"]
gtfs_path = path_dict["gtf_path"]
hunk_path = path_dict["hunk_path"]
irbl_path = path_dict["irbl_path"]
repos = os.listdir(bugs_path)
for repo in repos:
    log_one_lines = open(hunk_path+"\\"+repo+"\\logOneLine.txt", "r", encoding="utf8").readlines()
    commit_id_list = []
    commit_date_list = []
    commit_id_date_dict = {}
    commit_date_id_dict = {}
    for line in log_one_lines:
        tokens = line.split("\t")
        if len(tokens) < 3:
            continue
        commit_id = tokens[0]
        commit_date = tokens[2].split(" +")[0]
        commit_date = commit_date.split(" -")[0]
        commit_date = date_parser(commit_date)
        commit_id_list.append(commit_id)
        commit_date_list.append(commit_date)
        commit_id_date_dict[commit_id] = commit_date
        commit_date_id_dict[commit_date] = commit_id
    
    commit_key_map_lines = open(hunk_path+"\\"+repo+"\\000_commit\\commitKeyMap.txt", "r", encoding="utf8").readlines()
    commit_file_dict = {}
    file_name_dict = {}
    for line in commit_key_map_lines:
        line = line.replace("\n","")
        file_id = line.split("\t")[0]
        commit_id = line.split("\t")[1].split("|")[0]
        commit_file = line.split("\t")[1].split("|")[1].lower().replace("/","\\")

        if commit_id not in commit_file_dict.keys():
            commit_file_dict[commit_id] = []
        commit_file_dict[commit_id].append(file_id)

        if file_id in file_name_dict.keys():
            print(file_id)
        file_name_dict[file_id] = commit_file

    vers = os.listdir(bugs_path+repo+"\\")
    for ver in vers:
        files = os.listdir(files_path+repo+"\\"+ver+"\\")
        file_dict = {}
        file_dict_by_name = {}
        file_name_set= set()
        for file in files:
            if file.endswith(".txt") is False:
                continue
            lang = file.replace("KeyMap.txt", "").lower()
            file_path = files_path+repo+"\\"+ver+"\\"+file
            f = open(file_path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                if line.find("|") == -1:
                    continue
                file_id = lang+"-"+line.split("|")[0]
                file_name = line.split("|")[1].lower()
                file_dict[file_id] = file_name
                file_name_set.add(file_name)
                file_dict_by_name[file_name] = file_id
        bugs = os.listdir(bugs_path+repo+"\\"+ver+"\\")
        print(repo, ver, len(bugs), len(file_name_set))
        for bug in bugs:            
            bugid = bug.replace(".json","")        

            if os.path.exists(gtfs_path+repo+"\\"+ver+"\\"+bugid+".txt") is False:
                continue
            query_desc = ' '.join(open(query_path+repo+"\\"+ver+"\\"+bugid+"\\query_base-desc.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query_sum = ' '.join(open(query_path+repo+"\\"+ver+"\\"+bugid+"\\query_base-sum.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query = query_desc+" "+query_sum            

            contents = None
            with open(bugs_path+repo+"\\"+ver+"\\"+bug, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())
            output_path = irbl_path+"\\"+repo+"\\"+ver+"\\"+bugid+"\\commit_score\\"
            
            reporting_datetime = date_parser(contents['BR']['BRopenT'])
            reporting_time = time.mktime(reporting_datetime.timetuple())

            commit_index = -1
            for commit_date in commit_date_list:
                commit_index +=1
                commit_time = time.mktime(commit_date.timetuple())
                diff = reporting_time - commit_time
                if diff <= -1: 
                    continue
                else:
                    print(commit_index, diff,commit_date,reporting_datetime)
                    break

            corpus = []
            id_list = []
            target_commit_ids = commit_id_list[commit_index:]
            for target_commit_id in target_commit_ids:
                if target_commit_id not in commit_file_dict.keys():
                    continue
                target_file_ids = commit_file_dict[target_commit_id]
                for target_file_id in target_file_ids:
                    commit_file_name = file_name_dict[target_file_id]
                    if commit_file_name in file_name_set:
                        id_list.append(target_file_id)
                        hunk_pp = ' '.join(open(hunk_path+"\\"+repo+"\\000_commit\\logs_pp\\"+target_file_id+".txt", "r", encoding="utf8").readlines()).replace("\n"," ")
                        corpus.append(hunk_pp)

            if len(corpus) <=0:
                continue
            tokenized_corpus = [doc.split(" ") for doc in corpus]
            bm25_model = BM25Okapi(tokenized_corpus)
            bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, id_list, query)
            
            final_score = {}
            for id in id_list:
                ss_file_id = file_dict_by_name[file_name_dict[id]]        
                score = bm25_sim_scores[id]
                if ss_file_id not in final_score.keys():
                    final_score[ss_file_id] = 0
                if final_score[ss_file_id] < score:
                    final_score[ss_file_id] = score

                       
            output_path = irbl_path+"\\"+repo+"\\"+ver+"\\"+bugid+"\\commit_score\\"
            write_f = open(output_path+"bm25_hunk_sim.txt", "w", encoding="utf8")
            for ss_file_id in final_score.keys():
                # print(ss_file_id, final_score[ss_file_id])
                write_f.write(ss_file_id+"\t"+str(final_score[ss_file_id])+"\n")
            write_f.close()            
            print(output_path, len(corpus), len(bm25_sim_scores), len(final_score))