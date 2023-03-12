import os
import json
import datetime


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

files_path = path_dict["file_path"]
bugs_path = path_dict["bug_path"]
gtfs_path = path_dict["gtf_path"]
repos = os.listdir(bugs_path)
target_bug_num = 0
target_repo_num = 0
for repo in repos:
    versions = os.listdir(bugs_path+repo+"\\")
    project_bug_num = 0
    for version in versions:
        if os.path.exists(gtfs_path+repo+"\\"+version+"\\") is False:
            os.makedirs(gtfs_path+repo+"\\"+version+"\\")
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
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
        for bug in bugs:                      
            bug_path = bugs_path+repo+"\\"+version+"\\"+bug
            contents = None
            with open(bug_path, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())
            
            bug_id = bug.replace(".json","")
            changed_files = contents['commit']['changed_files']
            buggy_files = []
            buggy_file_ids = []
            file_type_set = set()
            for changed_file in changed_files:
                change_type = contents['commit']['changed_files'][changed_file]['file_change_type']
                if change_type != "MODIFY":
                    continue
                original_file_name = contents['commit']['changed_files'][changed_file]['file_old_name'].lower()
                if original_file_name not in file_name_set:
                    continue
                file_name = original_file_name.split("\\")
                file_name = file_name[len(file_name)-1]
                file_name_tokens = file_name.split(".")
                if len(file_name_tokens) > 1:
                    file_type = file_name_tokens[len(file_name_tokens)-1]
                elif len(file_name_tokens) == 1 and file_name != "none":
                    file_type = file_name_tokens[len(file_name_tokens)-1]
                buggy_file_ids.append(file_dict_by_name[original_file_name])
                buggy_files.append(original_file_name)
            print(repo, version, bug, buggy_file_ids)
            f = open(gtfs_path+repo+"\\"+version+"\\"+bug_id+".txt", "w", encoding="utf8")
            for buggy_file_id in buggy_file_ids:
                f.write(buggy_file_id+"\n")
            f.close()
            target_bug_num += 1
            project_bug_num += 1
    if project_bug_num > 0:
        target_repo_num += 1

print(target_repo_num, target_bug_num,project_bug_num)


