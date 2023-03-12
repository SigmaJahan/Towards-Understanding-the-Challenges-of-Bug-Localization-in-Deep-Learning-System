import os
import json
import datetime
import shutil
import math


k_days = [15, 30, 60, 90, 150]

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
files_path = path_dict["file_path"]
commit_path = path_dict["commit_path"]
irbl_path = path_dict["irbl_path"]
repos = os.listdir(bugs_path)
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    f = open(commit_path+"\\"+repo+".txt", "r", encoding="utf8")
    file_date_dict = {}
    for line in f.readlines():
        line = line.replace("\n","")
        file_name = line.split("\t")[0].lower()
        commit_date = line.split("\t")[1].split("|")
        if len(commit_date) == 0:
            continue
        if len(commit_date[0]) < 3:
            continue
        commit_datetime = []
        for date in commit_date:
            date = date.split(" ")[0]
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            commit_datetime.append(date_obj)
        file_date_dict[file_name] = commit_datetime
    print(repo, len(file_date_dict))

    for version in versions:
        files = os.listdir(files_path+repo+"\\"+version+"\\")
        file_dict = {}
        file_dict_by_name = {}
        file_name_set= set()
        for file in files:
            if file.endswith(".txt") is False:
                continue
            lang = file.replace("KeyMap.txt", "").lower()
            file_path = files_path+repo+"\\"+version+"\\"+file
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

        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
        for bug in bugs:   
            bugid = bug.replace(".json","")        
            contents = None
            with open(bugs_path+repo+"\\"+version+"\\"+bug, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())

            reporting_datetime = contents['BR']['BRopenT']
            reporting_date = reporting_datetime.split("T")[0]
            reporting_time = reporting_datetime.split("T")[1].replace("Z","")

            report_time_str = reporting_date
            report_time_obj = datetime.datetime.strptime(report_time_str, "%Y-%m-%d")

            if os.path.exists(irbl_path+"\\"+repo+"\\"+version+"\\"+bugid+"\\commit_score\\") is False:
                os.makedirs(irbl_path+"\\"+repo+"\\"+version+"\\"+bugid+"\\commit_score\\")
            score_f = open(irbl_path+"\\"+repo+"\\"+version+"\\"+bugid+"\\commit_score\\score.txt", "w", encoding="utf8")
            for file_name in file_date_dict.keys():
                if file_name not in file_dict_by_name.keys():
                    # print(repo, version, bugid, file_name, 'no in search space')
                    continue
                file_id = file_dict_by_name[file_name]              
                file_scores = ""
                for k in k_days:          
                    file_score = 0
                    commit_dates = file_date_dict[file_name]                    
                    for commit_date in commit_dates:
                        file_name = file_name.lower()
                        diff = report_time_obj-commit_date
                        if diff.days < 0:
                            continue                        
                        if diff.days <= k:   
                            diff_day = int(diff.days)
                            # print(k, diff_day,bugid,file_id, report_time_obj, commit_date)
                            upper = 12* (1- ((k-diff_day)/k))
                            score = 1 / (1 + math.exp(upper))
                            # print(score)
                            file_score += score
                    file_scores = file_scores + str(file_score)+"\t"
                score_f.write(file_id+"\t"+file_scores+"\n")  
            score_f.close()
        print(repo, version, len(bugs))