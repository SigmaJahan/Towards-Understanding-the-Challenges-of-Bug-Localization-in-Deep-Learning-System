import os
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util
import math 

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

query_num = {}
query_mrr = {}
query_map = {}
target_bug_num = 0
target_repo_num = 0
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0
    for version in versions:
        source_files = os.listdir(files_path+repo+"\\"+version+"\\python_pp\\")
        if len(source_files) == 0:
            continue
        file_corpus = []
        file_id_list = []
        for source_file in source_files:
            file_id = source_file.split(".")[len(source_file.split("."))-2]
            contents = ' '.join(open(files_path+repo+"\\"+version+"\\python_pp\\"+source_file, "r", encoding="utf8").readlines()).replace("\n"," ")
            file_corpus.append(contents)
            file_id_list.append("python-"+file_id)                
            
        tokenized_corpus = [doc.split(" ") for doc in file_corpus]
        bm25_model = BM25Okapi(tokenized_corpus)
    
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            query = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-desc.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query_sum = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-sum.txt", "r", encoding="utf8").readlines()).replace("\n","")
            base_query = query + " "+query_sum
            base_query = base_query.strip()
            lines = open(gtfs_path+repo+"\\"+version+"\\"+bug+".txt", "r", encoding="utf8").readlines()
            gtf_list = []
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_list.append(line)
            if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\query_sim\\") is False:
                os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\query_sim\\")

            query_list = os.listdir(bugs_path+repo+"\\"+version+"\\"+bug+"\\")
            for query_type in query_list:
                if query_type.find("query_") == -1:
                    continue

                specific_query =  ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\"+query_type, "r", encoding="utf8").readlines()).replace("\n","")
                
                # BASE
                reformulate_type = "BASE_"+query_type.replace(".txt","") 
                bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, file_id_list, base_query)
                bm25_top_rank, bm25_rr, bm25_ap, _, _  = ir_util.evaluation(bm25_sim_scores, gtf_list, len(file_corpus), 100000)
                # print(repo, version, bug, len(gtf_list), reformulate_type, bm25_rr, bm25_ap)
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\query_sim\\"+reformulate_type+".txt", "w", encoding="utf8")
                for file_id in bm25_sim_scores.keys():
                    f.write(file_id+"\t"+str(bm25_sim_scores[file_id])+"\n")
                f.close()

                if reformulate_type not in query_num.keys():
                    query_num[reformulate_type] = 0
                    query_mrr[reformulate_type] = 0
                    query_map[reformulate_type] = 0
                query_num[reformulate_type] += 1
                query_mrr[reformulate_type] += bm25_rr
                query_map[reformulate_type] += bm25_ap



                # SELECTION
                reformulate_type = "SEL_"+query_type.replace(".txt","")                
                
                bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, file_id_list, specific_query)
                bm25_top_rank, bm25_rr, bm25_ap, _, _  = ir_util.evaluation(bm25_sim_scores, gtf_list, len(file_corpus), 100000)
                # print(repo, version, bug, len(gtf_list), reformulate_type, bm25_rr, bm25_ap)
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\query_sim\\"+reformulate_type+".txt", "w", encoding="utf8")
                for file_id in bm25_sim_scores.keys():
                    f.write(file_id+"\t"+str(bm25_sim_scores[file_id])+"\n")
                f.close()

                if reformulate_type not in query_num.keys():
                    query_num[reformulate_type] = 0
                    query_mrr[reformulate_type] = 0
                    query_map[reformulate_type] = 0
                query_num[reformulate_type] += 1
                query_mrr[reformulate_type] += bm25_rr
                query_map[reformulate_type] += bm25_ap


                #REDUCTION
                reformulate_type = "RED_"+query_type.replace(".txt","")

                specific_tokens = specific_query.split(" ")
                reduced_query = " "+base_query+" "
                for token in specific_tokens:
                    reduced_query = reduced_query.replace(" "+token+" "," ",1)
                reduced_query = reduced_query.strip()

                bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, file_id_list, reduced_query)
                bm25_top_rank, bm25_rr, bm25_ap, _, _  = ir_util.evaluation(bm25_sim_scores, gtf_list, len(file_corpus), 100000)
                # print(repo, version, bug, len(gtf_list), reformulate_type, bm25_rr, bm25_ap)
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\query_sim\\"+reformulate_type+".txt", "w", encoding="utf8")
                for file_id in bm25_sim_scores.keys():
                    f.write(file_id+"\t"+str(bm25_sim_scores[file_id])+"\n")
                f.close()

                if reformulate_type not in query_num.keys():
                    query_num[reformulate_type] = 0
                    query_mrr[reformulate_type] = 0
                    query_map[reformulate_type] = 0
                query_num[reformulate_type] += 1
                query_mrr[reformulate_type] += bm25_rr
                query_map[reformulate_type] += bm25_ap            
            
            target_bug_num += 1
            project_bug_num += 1
        
    if project_bug_num > 0:
        target_repo_num += 1
        for key in query_num.keys():
            bug_num = query_num[key]
            mrr = query_mrr[key]
            map = query_map[key]
            print(repo, key, bug_num, round(mrr/bug_num,3), round(map/bug_num,3))

print(target_repo_num, target_bug_num, project_bug_num)