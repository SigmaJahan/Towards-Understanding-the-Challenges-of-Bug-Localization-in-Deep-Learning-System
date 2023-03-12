import os
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util
import math 
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import re

file_path_reg = re.compile('(?:\/[a-z]+\/)(.+?)(?:\/.+)(\.py|\.cpp|\.hpp|\.cc|\.java|\.cs|\.js|\.ts|\.go|\.cs|\.scala|\.c|\.h)')

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

bugs_path = path_dict["query_path"]
files_path = path_dict["file_path"]
gtfs_path = path_dict["gtf_path"]
irbl_path = path_dict["irbl_path"]
repos = os.listdir(bugs_path)

mrr_vsm = 0
map_vsm = 0
mrr_rvsm = 0
map_rvsm = 0
mrr_bm = 0
map_bm = 0
target_bug_num = 0
target_repo_num = 0
trace_bug_num = 0
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0

    for version in versions:
        possible_file_path_list = []
        possible_file_path_dict = {}
        files = os.listdir(files_path+repo+"\\"+version+"\\")
        lang_types = set()
        for file in files:
            if file.endswith(".txt") is False:
                continue
            lang = file.replace("KeyMap.txt", "").lower()
            file_path = files_path+repo+"\\"+version+"\\"+file
            f = open(file_path, "r", encoding="utf8")
            lines = f.readlines()
            if len(lines) > 0:
                lang_types.add(lang)
            for line in lines:
                file_id = lang+"-"+line.replace("\n","").split("|")[0]
                search_space_file_path = line.replace("\n","").split("|")[1].replace("\\","/").lower()
                possible_file_path_list.append(search_space_file_path)
                possible_file_path_dict[search_space_file_path] = file_id
        if len(lang_types) == 0:
            continue
    
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            if os.path.exists(bugs_path+repo+"\\"+version+"\\"+bug+"\\raw_data-strace.txt") is False:
                continue

            traces = open(bugs_path+repo+"\\"+version+"\\"+bug+"\\raw_data-strace.txt", "r", encoding="utf8").readlines()

            file_path_list = []
            file_paht_lang_type = set()
            for trace in traces:                
                trace = trace.replace("\n","")      
                trace = trace.replace("\\\\","/")
                trace = trace.replace("\\","/")          
                groups =  file_path_reg.search(trace)                
                if groups != None:
                    strace_text = groups.group().lower()
                    file_path_list.append(strace_text)            

            if len(file_path_list) > 0:                   
                file_path_list.reverse()
                # print(file_path_list)

                rank = 1.0
                file_score_dict = {}
                for file_path in file_path_list:
                    new_file_path = file_path.replace("/site-packages/","/python/")
                    repo_token = repo.split("+")[1]
                    if new_file_path.find("/python/") > -1:
                        new_file_path = new_file_path.split("/python/")[1]                    
                    elif new_file_path.find("/"+repo_token+"/") > -1:
                        new_file_path = new_file_path.split("/"+repo_token+"/")[1]
                    candidate_path = set()                             
                    for possible_path in possible_file_path_list:     
                        if possible_path.endswith(new_file_path) is True:
                            candidate_path.add(possible_path)
                    if len(candidate_path) == 0:
                        continue

                    if rank <= 10.0:
                        score = 1.0/rank
                    else:
                        score = 0.1

                    for path in candidate_path:
                        file_id = possible_file_path_dict[path]
                        if file_id not in file_score_dict.keys():
                            file_score_dict[file_id] = score

                      #  print(path, score)
                    rank += 1.0

                if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\strace_sim\\") is False:
                    os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\strace_sim\\")
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\strace_sim\\strace_score.txt", "w", encoding="utf8")                
                for file_id in file_score_dict.keys():
                    score = file_score_dict[file_id]
                    f.write(file_id+"\t"+str(score)+"\n")
                f.close()
                trace_bug_num += 1  
                print(repo, bug)
            

print(trace_bug_num)