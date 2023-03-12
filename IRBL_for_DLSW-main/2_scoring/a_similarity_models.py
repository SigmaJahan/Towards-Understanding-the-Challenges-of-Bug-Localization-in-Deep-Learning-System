import os
import sklearn
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
print(irbl_path)
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
    for version in versions:
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
        if len(lang_types) == 0:
            continue

        lang_files = {}
        lang_file_ids = {}
        lang_tfidf = {}
        lang_vectorizer = {}
        lang_bm25 = {}
        lang_length_scores = {}
        for lang_type in lang_types:
            source_files = os.listdir(files_path+repo+"\\"+version+"\\"+lang_type+"_pp\\")
            file_corpus = []
            file_id_list = []
            lengths = []
            max_length = 0
            min_length = 99999
            for source_file in source_files:
                file_id = source_file.split(".")[len(source_file.split("."))-2]
                contents = ' '.join(open(files_path+repo+"\\"+version+"\\"+lang_type+"_pp\\"+source_file, "r", encoding="utf8").readlines()).replace("\n"," ")
                file_corpus.append(contents)
                file_id_list.append(lang_type+"-"+file_id)
                length = len(contents.split())
                lengths.append(length)
                if max_length < length:
                    max_length = length
                if min_length > length:
                    min_length = length
            
            length_score_dict = {}
            for i in range(len(file_id_list)):
                length = lengths[i]
                file_id = file_id_list[i]
                if max_length == min_length:
                    length= 1
                else:
                    length = (length - min_length) / (max_length - min_length)
                if length == 0:
                    length = 1
                length_score = 1 / (1 + math.exp(-length))
                if length_score == 0:
                    length_score = 1
                length_score_dict[file_id] = length_score
            if max_length <= 3 :
                continue
            
            lang_files[lang_type] = file_corpus
            lang_file_ids[lang_type] = file_id_list


            vectorizer = TfidfVectorizer(stop_words='english', max_features = 10000)
            file_tfidf = vectorizer.fit_transform(file_corpus)
            lang_tfidf[lang_type] = file_tfidf
            lang_vectorizer[lang_type] = vectorizer

            tokenized_corpus = [doc.split(" ") for doc in file_corpus]
            bm25_model = BM25Okapi(tokenized_corpus)
            lang_bm25[lang_type] = bm25_model

            lang_length_scores[lang_type] = length_score_dict
    
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            query = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-desc.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query_sum = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-sum.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query = query + " "+query_sum
            query = query.strip()
            lines = open(gtfs_path+repo+"\\"+version+"\\"+bug+".txt", "r", encoding="utf8").readlines()
            gtf_list = []
            lang_set = set()
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_list.append(line)
                lang = line.split("-")[0]
                lang_set.add(lang)
            if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\sf_sim\\") is False:
                os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\sf_sim\\")
            for lang in lang_set:
                file_ids = lang_file_ids[lang]
                files_corpus = lang_files[lang]
                vectorizer = lang_vectorizer[lang]
                file_tfidf = lang_tfidf[lang]
                bm_25 = lang_bm25[lang]
                lang_gtf_list = []
                for gtf in gtf_list:
                    if str(gtf).startswith(lang) is True:
                        lang_gtf_list.append(gtf.split("-")[1])
                if len(lang_gtf_list) == 0:
                    continue
                vsm_sim_scores = ir_util.retrieval_tfidf(vectorizer, file_tfidf, file_ids, query)
                vsm_top_rank, vsm_rr, vsm_ap, _, _  = ir_util.evaluation(vsm_sim_scores, gtf_list, len(files_corpus), 100000) 

                length_score_dict = lang_length_scores[lang]
                rvsm_sim_scores = ir_util.retrieval_tfidf_revised(vectorizer, file_tfidf, file_ids, query, length_score_dict)
                rvsm_top_rank, rvsm_rr, rvsm_ap, _, _  = ir_util.evaluation(rvsm_sim_scores, gtf_list, len(files_corpus), 100000) 


                bm25_sim_scores = ir_util.retrieval_bm25(bm_25, file_ids, query)
                bm25_top_rank, bm25_rr, bm25_ap, _, _  = ir_util.evaluation(bm25_sim_scores, gtf_list, len(files_corpus), 100000)
                print(repo, version, bug, len(gtf_list), vsm_rr, vsm_ap, rvsm_rr, rvsm_ap, bm25_rr, bm25_ap)

                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\sf_sim\\"+lang+"_vsm.txt", "w", encoding="utf8")
                for file_id in vsm_sim_scores.keys():
                    f.write(file_id+"\t"+str(vsm_sim_scores[file_id])+"\n")
                f.close()
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\sf_sim\\"+lang+"_rvsm.txt", "w", encoding="utf8")
                for file_id in rvsm_sim_scores.keys():
                    f.write(file_id+"\t"+str(rvsm_sim_scores[file_id])+"\n")
                f.close()
                f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\sf_sim\\"+lang+"_bm25.txt", "w", encoding="utf8")
                for file_id in bm25_sim_scores.keys():
                    f.write(file_id+"\t"+str(bm25_sim_scores[file_id])+"\n")
                f.close()
                
                
                mrr_vsm += vsm_rr
                map_vsm += vsm_ap
                mrr_rvsm += rvsm_rr
                map_rvsm += rvsm_ap
                mrr_bm += bm25_rr
                map_bm += bm25_ap

                target_bug_num += 1
                project_bug_num += 1
                
    if project_bug_num > 0:
        target_repo_num += 1

print(target_repo_num, target_bug_num, project_bug_num)
print(mrr_vsm/target_bug_num, mrr_rvsm/target_bug_num, mrr_bm/target_bug_num,map_vsm/target_bug_num, map_rvsm/target_bug_num, map_bm/target_bug_num )



