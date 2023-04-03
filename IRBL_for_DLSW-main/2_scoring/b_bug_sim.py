import os
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util
import math 
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi


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
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0

    br_query_dict = {}
    br_gtf_dict = {}
    br_ver_dict = {}
    file_ver_dict = {}
    for version in versions:
        file_key_dict = {}
        file_name_dict = {}
        lines = open(files_path+"\\"+repo+"\\"+version+"\\pythonKeyMap.txt","r", encoding="utf8").readlines()
        for line in lines:
            line = line.replace("\n","")
            file_id = "python-"+line.split("|")[0]
            file_name = line.split("|")[1]
            file_key_dict[file_id] = file_name
            file_name_dict[file_name] = file_id
        file_ver_dict[version+"_KEYDICT"] = file_key_dict
        file_ver_dict[version+"_NAMEDICT"] = file_name_dict

        
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            bug_id = int(bug)
            query = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-desc.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query = query +' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-sum.txt", "r", encoding="utf8").readlines()).replace("\n","")
            lines = open(gtfs_path+repo+"\\"+version+"\\"+bug+".txt", "r", encoding="utf8").readlines()
            gtf_list = []            
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_list.append(line)
                lang = line.split("-")[0]
            
            br_query_dict[bug_id] = query
            br_gtf_dict[bug_id] = gtf_list
            br_ver_dict[bug_id] = version


    print(repo, len(br_query_dict))
    for bug_id, query in sorted(br_query_dict.items()):        
        sim_corpus = []
        sim_id_list = []
        sim_gtf_dict = {}
        for past_bug_id, sim_query in sorted(br_query_dict.items()):
            if bug_id <= past_bug_id:
                continue
            sim_query = br_query_dict[past_bug_id]      
            sim_corpus.append(sim_query)
            sim_id_list.append(past_bug_id)
            gtf_list = br_gtf_dict[past_bug_id]
            sim_gtf_dict[past_bug_id] = gtf_list
        if len(sim_corpus) == 0:
            if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\") is False:
                os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\")
            f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\bm25.txt", "w", encoding="utf8")            
            f.close()
            continue

        tokenized_corpus = [doc.split(" ") for doc in sim_corpus]
        bm25_model = BM25Okapi(tokenized_corpus)
        bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, sim_id_list, query)
        
        if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\") is False:
            os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\")        

        print(repo,version, bug_id, len(sim_id_list))    

        file_score_dict = {}
        for past_bug_id in bm25_sim_scores.keys():
            sim_score = bm25_sim_scores[past_bug_id]
            gtf_list = sim_gtf_dict[past_bug_id]
            past_bug_ver = br_ver_dict[past_bug_id]
            file_id_dict = file_ver_dict[past_bug_ver+"_KEYDICT"]
            past_bug_file_name = set()
            for gtf_id in gtf_list:
                gtf_name = file_id_dict[gtf_id]
                past_bug_file_name.add(gtf_name)
            
            new_gtf_list = []
            file_name_dict = file_ver_dict[version+"_NAMEDICT"]
            for gtf_name in past_bug_file_name:
                if gtf_name not in file_name_dict.keys():
                    print(gtf_name, bug_id, past_bug_id)
                else:
                    new_gtf_list.append(file_name_dict[gtf_name])
            
            gtf_list = new_gtf_list
            file_score = sim_score / len(gtf_list)
            for gtf in gtf_list:
                if gtf not in file_score_dict.keys():
                    file_score_dict[gtf] = 0
                file_score_dict[gtf] += file_score

        f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+str(bug_id)+"\\br_sim\\bm25.txt", "w", encoding="utf8")
        for sf_id in file_score_dict.keys():
            score = file_score_dict[sf_id]
            f.write(sf_id+"\t"+str(score)+"\n")
        f.close()