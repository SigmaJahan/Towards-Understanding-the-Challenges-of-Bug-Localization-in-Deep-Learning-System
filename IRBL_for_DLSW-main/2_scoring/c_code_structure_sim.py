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

repos = os.listdir(bugs_path)

mrr_bm = 0
map_bm = 0
target_bug_num = 0
target_repo_num = 0
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0
    for version in versions:
        files_path = path_dict["file_path"]
        methods_path = path_dict["function_path"]
        class_path = path_dict["class_path"]
        variable_path = path_dict["variable_path"]
        comment_path = path_dict["comment_path"]
        files = os.listdir(methods_path+repo+"\\"+version+"\\")
        classes = os.listdir(class_path+repo+"\\"+version+"\\")
        variables = os.listdir(variable_path+repo+"\\"+version+"\\")
        comments = os.listdir(comment_path+repo+"\\"+version+"\\")

        files_dict = {}
        files_dict_by_name = {}
        files_name_set= set()

        methods_dict = {}
        methods_dict_by_name = {}
        methods_name_set= set()

        class_dict = {}
        class_dict_by_name = {}
        class_name_set= set()

        variable_dict = {}
        variable_dict_by_name = {}
        variable_name_set= set()

        comment_dict = {}
        comment_dict_by_name = {}
        comment_name_set= set()

        for file in files:
            if file.endswith(".txt") is False:
                continue
            lang = file.replace("KeyMap.txt", "").lower()

            files_path = methods_path+repo+"\\"+version+"\\"+file
            f = open(files_path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                if line.find("|") == -1:
                    continue
                tokens = line.split("|")
                file_id = tokens[0]
                file_name = tokens[1].lower().replace("\\\\","\\")
                files_dict[file_id] = file_name
                files_name_set.add(file_name)
                files_dict_by_name[file_name] = file_id

                method_id = file_id+"|"+tokens[2]
                method_name = file_name+"|"+tokens[3].lower()
                methods_dict[method_id] = method_name
                methods_name_set.add(method_name)
                methods_dict_by_name[method_name] = method_id
        
        for class_file in classes:
            if class_file.endswith(".txt") is False:
                continue
            lang = class_file.replace("KeyMap.txt", "").lower()
            class_path = class_path+repo+"\\"+version+"\\"+class_file
            f = open(class_path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                if line.find("|") == -1:
                    continue
                tokens = line.split("|")
                file_id = tokens[0]
                file_name = tokens[1].lower().replace("\\\\","\\")
                files_dict[file_id] = file_name
                files_name_set.add(file_name)
                files_dict_by_name[file_name] = file_id

                class_id = file_id+"|"+tokens[2]
                class_name = file_name+"|"+tokens[3].lower()
                class_dict[class_id] = class_name
                class_name_set.add(class_name)
                class_dict_by_name[class_name] = class_id
        
        for variable_file in variables:
            if variable_file.endswith(".txt") is False:
                continue
            lang = variable_file.replace("KeyMap.txt", "").lower()
            variable_path = variable_path+repo+"\\"+version+"\\"+variable_file
            f = open(variable_path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                if line.find("|") == -1:
                    continue
                tokens = line.split("|")
                file_id = tokens[0]
                file_name = tokens[1].lower().replace("\\\\","\\")
                files_dict[file_id] = file_name
                files_name_set.add(file_name)
                files_dict_by_name[file_name] = file_id

                variable_id = file_id+"|"+tokens[2]
                variable_name = file_name+"|"+tokens[3].lower()
                variable_dict[variable_id] = variable_name
                variable_name_set.add(variable_name)
                variable_dict_by_name[variable_name] = variable_id
        
        for comment_file in comments:
            if comment_file.endswith(".txt") is False:
                continue
            lang = comment_file.replace("KeyMap.txt", "").lower()
            comment_path = comment_path+repo+"\\"+version+"\\"+comment_file
            f = open(comment_path, "r", encoding="utf8")
            lines = f.readlines()
            for line in lines:
                line = line.replace("\n","")
                if line.find("|") == -1:
                    continue
                tokens = line.split("|")
                file_id = tokens[0]
                file_name = tokens[1].lower().replace("\\\\","\\")
                files_dict[file_id] = file_name
                files_name_set.add(file_name)
                files_dict_by_name[file_name] = file_id

                if len(tokens) <= 2:
                    continue
                comment_id = file_id+"|"+tokens[2]
                comment_name = file_name+"|"+tokens[-1].lower()
                comment_dict[comment_id] = comment_name
                comment_name_set.add(comment_name)
                comment_dict_by_name[comment_name] = comment_id
        files_path = path_dict["file_path"]
        methods_path = path_dict["function_path"]
        class_path = path_dict["class_path"]
        variable_path = path_dict["variable_path"]
        comment_path = path_dict["comment_path"]
        methods = os.listdir(function_path+repo+"\\"+version+"\\python_pp\\")
        if len(methods) == 0:
            continue
        method_corpus = []
        method_id_list = []
        lengths = []
        max_length = 0
        min_length = 99999
        for method in methods:
            method_id = method.split(".")[0]
            contents = ' '.join(open(function_path+repo+"\\"+version+"\\python_pp\\"+method, "r", encoding="utf8").readlines()).replace("\n"," ")
            method_corpus.append(contents)
            method_id_list.append("python-"+method_id)
        tokenized_corpus = [doc.split(" ") for doc in method_corpus]
        bm25_model = BM25Okapi(tokenized_corpus)

        classes = os.listdir(class_path+repo+"\\"+version+"\\python_pp\\")
        if len(classes) == 0:
            continue
        class_corpus = []
        class_id_list = []
        for class_ in classes:
            class_id = class_.split(".")[0]
            contents = ' '.join(open(class_path+repo+"\\"+version+"\\python_pp\\"+class_, "r", encoding="utf8").readlines()).replace("\n"," ")
            class_corpus.append(contents)
            class_id_list.append("python-"+class_id)
        tokenized_corpus = [doc.split(" ") for doc in class_corpus]
        bm25_class_model = BM25Okapi(tokenized_corpus)

        variable = os.listdir(variable_path+repo+"\\"+version+"\\python_pp\\")
        if len(variable) == 0:
            continue
        variable_corpus = []
        variable_id_list = []
        for var in variable:
            variable_id = var.split(".")[0]
            contents = ' '.join(open(variable_path+repo+"\\"+version+"\\python_pp\\"+var, "r", encoding="utf8").readlines()).replace("\n"," ")
            variable_corpus.append(contents)
            variable_id_list.append("python-"+variable_id)
        tokenized_corpus = [doc.split(" ") for doc in variable_corpus]
        bm25_variable_model = BM25Okapi(tokenized_corpus)

        comments = os.listdir(comment_path+repo+"\\"+version+"\\python_pp\\")
        if len(comments) == 0:
            continue
        comment_corpus = []
        comment_id_list = []
        for comment in comments:
            comment_id = comment.split(".")[0]
            contents = ' '.join(open(comment_path+repo+"\\"+version+"\\python_pp\\"+comment, "r", encoding="utf8").readlines()).replace("\n"," ")
            comment_corpus.append(contents)
            comment_id_list.append("python-"+comment_id)
        tokenized_corpus = [doc.split(" ") for doc in comment_corpus]
        bm25_comment_model = BM25Okapi(tokenized_corpus)

        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+".txt") is False:
                continue
            query = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-desc.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query_sum = ' '.join(open(bugs_path+repo+"\\"+version+"\\"+bug+"\\query_base-sum.txt", "r", encoding="utf8").readlines()).replace("\n","")
            query = query + " "+query_sum
            query = query.strip()
            if os.path.exists(gtfs_path+repo+"\\"+version+"\\"+bug+"_method.txt") is False:
                continue
            lines = open(gtfs_path+repo+"\\"+version+"\\"+bug+"_method.txt", "r", encoding="utf8").readlines()
            gtf_method_list = []
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_method_list.append(line)
            
            lines = open (gtfs_path+repo+"\\"+version+"\\"+bug+"_class.txt", "r", encoding="utf8").readlines()
            gtf_class_list = []
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_class_list.append(line)
            
            lines = open (gtfs_path+repo+"\\"+version+"\\"+bug+"_variable.txt", "r", encoding="utf8").readlines()
            gtf_variable_list = []
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_variable_list.append(line)
            
            lines = open (gtfs_path+repo+"\\"+version+"\\"+bug+"_comment.txt", "r", encoding="utf8").readlines()
            gtf_comment_list = []
            for line in lines:
                line = line.replace("\n","")
                if len(line) < 3:
                    continue
                gtf_comment_list.append(line)

            if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\") is False:
                os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\")

            if len(gtf_method_list) == 0:
                continue

            bm25_sim_scores = ir_util.retrieval_bm25(bm25_model, method_id_list, query)
            bm25_top_rank, bm25_rr, bm25_ap, _, _  = ir_util.evaluation(bm25_sim_scores, gtf_method_list, len(method_corpus), 100000)

            bm25_sim_class_scores = ir_util.retrieval_bm25(bm25_class_model, class_id_list, query)
            bm25_top_rank_class, bm25_rr_class, bm25_ap_class, _, _  = ir_util.evaluation(bm25_sim_class_scores, gtf_class_list, len(class_corpus), 100000)

            bm25_sim_variable_scores = ir_util.retrieval_bm25(bm25_variable_model, variable_id_list, query)
            bm25_top_rank_variable, bm25_rr_variable, bm25_ap_variable, _, _  = ir_util.evaluation(bm25_sim_variable_scores, gtf_variable_list, len(variable_corpus), 100000)

            bm25_sim_comment_scores = ir_util.retrieval_bm25(bm25_comment_model, comment_id_list, query)
            bm25_top_rank_comment, bm25_rr_comment, bm25_ap_comment, _, _  = ir_util.evaluation(bm25_sim_comment_scores, gtf_comment_list, len(comment_corpus), 100000)

            print(repo, version, bug, bm25_rr, bm25_ap)

            a = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_method.txt", "w", encoding="utf8")
            b = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_class.txt", "w", encoding="utf8")
            c = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_variable.txt", "w", encoding="utf8")
            d = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bug+"\\mth_sim\\python_bm25_comment.txt", "w", encoding="utf8")
            for method_id in bm25_sim_scores.keys():
                a.write(method_id+"\t"+str(bm25_sim_scores[method_id])+"\n")
            
            for class_id in bm25_sim_class_scores.keys():
                b.write(class_id+"\t"+str(bm25_sim_class_scores[class_id])+"\n")
            
            for variable_id in bm25_sim_variable_scores.keys():
                c.write(variable_id+"\t"+str(bm25_sim_variable_scores[variable_id])+"\n")
            
            for comment_id in bm25_sim_comment_scores.keys():
                d.write(comment_id+"\t"+str(bm25_sim_comment_scores[comment_id])+"\n")
            
            a.close()
            b.close()
            c.close()
            d.close()

            mrr_bm += bm25_rr
            map_bm += bm25_ap

            target_bug_num += 1
            project_bug_num += 1

                
    if project_bug_num > 0:
        target_repo_num += 1

    print(target_repo_num, target_bug_num, project_bug_num)
    print(mrr_bm/target_bug_num,map_bm/target_bug_num)
