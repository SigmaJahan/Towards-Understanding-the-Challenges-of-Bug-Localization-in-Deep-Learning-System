import os
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util
import math 


def loader():
    path_dict = {}
    lines = open("C:\\Users\\sigma\\Desktop\\ICSME-2023\\IRBL_for_DLSW-main\\IRBL_for_DLSW-main\\2_scoring\\z_config.txt","r", encoding="utf8").readlines()
    for line in lines:
        line = line.replace("\n","")
        tokens = line.split("=",2)
        label = tokens[0]
        path = tokens[1]
        path_dict[label] = path
    return path_dict

path_dict = loader()
bugs_path = path_dict["query_path"]
function_path = path_dict["function_path"]
class_path = path_dict["class_path"]
variable_path = path_dict["variable_path"]
comment_path = path_dict["comment_path"]
gtfs_path = path_dict["gtf_path"]
irbl_path = path_dict["irbl_path"]
file_path = path_dict["file_path"]

repos = os.listdir(bugs_path)

mrr_bm = 0
map_bm = 0
target_bug_num = 0
target_repo_num = 0
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0
    for version in versions:
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            bm25_file_keymap = {}
            with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\bm25_final.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split('\t')
                    bm25_file_keymap[key.replace("python-", "")] = value
            bm25_sf_keymap = {}
            with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\sf_sim\\python_bm25.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split('\t')
                    bm25_sf_keymap[key.replace("python-", "")] = value
            
            bm25_br_keymap = {}
            with open(irbl_path + repo + "\\" + version + "\\" + bug + "\\br_sim\\bm25.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split('\t')
                    bm25_br_keymap[key.replace("python-", "")] = value
            
            bluir_bm25_keymap = {}
            for key in bm25_sf_keymap:
                bm25_value = float(bm25_sf_keymap[key])
                if key in bm25_file_keymap:
                    bm25_value += float(bm25_file_keymap[key])
                if key in bm25_br_keymap:
                    bm25_value += float(bm25_br_keymap[key])
                bluir_bm25_keymap[key] = bm25_value
            
            buglocator_rvsm_keymap = {}
            
            f = open (irbl_path + repo + "\\" + version + "\\" + bug + "\\bluir_bm25_score.txt", "w")
            for key in bluir_bm25_keymap:
                value = bluir_bm25_keymap[key]
                key = "python-" + key
                f.write(key + "\t" + str(value) + "\n")
            target_bug_num += 1
            project_bug_num += 1
    if project_bug_num > 0:
        target_repo_num += 1
