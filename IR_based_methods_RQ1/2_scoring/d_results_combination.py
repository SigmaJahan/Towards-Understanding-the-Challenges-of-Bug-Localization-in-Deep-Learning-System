import os
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import util.ir_util as ir_util
import math 


def loader():
    path_dict = {}
    lines = open("C:\\Users\\Desktop\\ICSME-2023\\IRBL_for_DLSW-main\\IRBL_for_DLSW-main\\2_scoring\\z_config.txt","r", encoding="utf8").readlines()
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
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            bm25_class_keymap = {}
            # Check if the file exists
            if os.path.exists(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_class.txt") is True:
                with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_class.txt", 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        key, value = line.strip().split('\t')
                        bm25_class_keymap[key.replace("python-", "")] = value

            class_keymap = {}
            if os.path.exists(class_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt") is True:
                with open(class_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt", "r", encoding="utf8") as file:
                    lines = file.readlines()
                    for line in lines:
                        tokens = line.strip().split('|')
                        if tokens[0] in class_keymap:
                            class_keymap[tokens[0]].append(tokens[-2])
                        else:
                            class_keymap[tokens[0]] = []
                            class_keymap[tokens[0]].append(tokens[-2])

            final_bm25_class_keymap = {}
            for key in class_keymap:
                final_bm25_class_keymap[key] = 0.0
                for keys in class_keymap[key]:
                    # Check if the key exists
                    if keys in bm25_class_keymap:
                        final_bm25_class_keymap[key] += float(bm25_class_keymap[keys])
            
            bm25_function_keymap = {}
            if os.path.exists(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_method.txt") is True:
                with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_method.txt", 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        key, value = line.strip().split('\t')
                        bm25_function_keymap[key.replace("python-", "")] = value
            
            function_keymap = {}
            if os.path.exists(function_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt") is True:
                with open(function_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt", "r", encoding="utf8") as file:
                    lines = file.readlines()
                    for line in lines:
                        tokens = line.strip().split('|')
                        if tokens[0] in function_keymap:
                            function_keymap[tokens[0]].append(tokens[-2])
                        else:
                            function_keymap[tokens[0]] = []
                            function_keymap[tokens[0]].append(tokens[-2])
            
            final_bm25_function_keymap = {}
            for key in function_keymap:
                final_bm25_function_keymap[key] = 0.0
                for keys in function_keymap[key]:
                    if keys in bm25_function_keymap:
                        final_bm25_function_keymap[key] += float(bm25_function_keymap[keys])
            
            bm25_variable_keymap = {}
            if os.path.exists(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_variable.txt") is True:
                with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_variable.txt", 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        key, value = line.strip().split('\t')
                        bm25_variable_keymap[key.replace("python-", "")] = value
            
            variable_keymap = {}
            if os.path.exists(variable_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt") is True:
                with open(variable_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt", "r", encoding="utf8") as file:
                    lines = file.readlines()
                    for line in lines:
                        tokens = line.strip().split('|')
                        if tokens[0] in variable_keymap:
                            variable_keymap[tokens[0]].append(tokens[2])
                        else:
                            variable_keymap[tokens[0]] = []
                            variable_keymap[tokens[0]].append(tokens[2])
            
            final_bm25_variable_keymap = {}
            for key in variable_keymap:
                final_bm25_variable_keymap[key] = 0.0
                for keys in variable_keymap[key]:
                    if keys in bm25_class_keymap:
                        final_bm25_variable_keymap[key] += float(bm25_variable_keymap[keys])
            
            bm25_comment_keymap = {}
            if os.path.exists(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_comment.txt") is True:
                with open(irbl_path+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_comment.txt", 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        key, value = line.strip().split('\t')
                        bm25_comment_keymap[key.replace("python-", "")] = value
            
            comment_keymap = {}
            if os.path.exists(comment_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt") is True:
                with open(comment_path+"\\"+repo+"\\"+version+"\\PythonKeyMap.txt", "r", encoding="utf8") as file:
                    lines = file.readlines()
                    for line in lines:
                        tokens = line.strip().split('|')
                        if len(tokens) >= 3 and tokens[0] in comment_keymap:
                            comment_keymap[tokens[0]].append(tokens[2])
                        elif len(tokens) >= 3:
                            comment_keymap[tokens[0]] = []
                            comment_keymap[tokens[0]].append(tokens[2])
            
            final_bm25_comment_keymap = {}
            for key in comment_keymap:
                final_bm25_comment_keymap[key] = 0.0
                for keys in comment_keymap[key]:
                    if keys in bm25_class_keymap:
                        final_bm25_comment_keymap[key] += float(bm25_comment_keymap[keys])
            
            final_bm25_keymap = {}
            if os.path.exists(file_path + "\\" + repo + "\\" + version + "\\PythonKeyMap.txt") is True:
                with open (file_path + "\\" + repo + "\\" + version + "\\PythonKeyMap.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        key = line.strip().split('|')[0]
                        final_bm25_keymap[key] = 0.0
                        if key in final_bm25_class_keymap:
                            final_bm25_keymap[key] += final_bm25_class_keymap[key]
                        if key in final_bm25_function_keymap:
                            final_bm25_keymap[key] += final_bm25_function_keymap[key]
                        if key in final_bm25_variable_keymap:
                            final_bm25_keymap[key] += final_bm25_variable_keymap[key]
                        if key in final_bm25_comment_keymap:
                            final_bm25_keymap[key] += final_bm25_comment_keymap[key]
            
            if os.path.exists(irbl_path + repo + "\\" + version + "\\" + bug) is True:
                f = open (irbl_path + repo + "\\" + version + "\\" + bug + "\\bm25_final.txt", "w")
            for key in final_bm25_keymap:
                value = final_bm25_keymap[key]
                key = "python-" + key
                f.write(key + "\t" + str(value) + "\n")
            f.close()
            target_bug_num += 1
            project_bug_num += 1
    if project_bug_num > 0:
        target_repo_num += 1
