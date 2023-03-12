import os
import subprocess
import datetime
import json

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
base_path = path_dict["bug_path"]
files_path = path_dict["file_path"]
commits_path = path_dict["commit_path"]
if os.path.exists(commits_path) is False:
    os.makedirs(commits_path)
gitrepo_path = path_dict["git_path"]
repos = os.listdir(base_path)
target_bug_num = 0
for repo in repos:
    candidate_file_list = set()
    versions =os.listdir(base_path+repo)
    for version in versions:
        bugs = os.listdir(base_path+repo+"\\"+version+"\\")
        files = os.listdir(files_path+repo+"\\"+version+"\\")
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
                file_name_set.add(file_name)

        for bug in bugs:                      
            bug_path = base_path+repo+"\\"+version+"\\"+bug
            contents = None
            with open(bug_path, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())
            
            bug_id = bug.replace(".json","")
            changed_files = contents['commit']['changed_files']
            buggy_files = []
            buggy_file_ids = []
            file_type_set = set()

            flag = False
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
                file_type = "[NONE]"
                if len(file_name_tokens) > 1:
                    file_type = file_name_tokens[len(file_name_tokens)-1]
                elif len(file_name_tokens) == 1 and file_name != "none":
                    file_type = file_name_tokens[len(file_name_tokens)-1]
                file_type = file_type.lower()
                candidate_file_list.add(original_file_name)
                flag = True
            if flag is True:
                target_bug_num+= 1
    print(repo, len(candidate_file_list))

    git_path = gitrepo_path+"\\"+repo+"\\"
    dir = os.listdir(git_path)[0]
    git_path = git_path + dir+"\\"    
    os.chdir(git_path)
    print(git_path)

    p = subprocess.Popen("cmd /u /c git checkout master --force", stdout=subprocess.PIPE)
    result = p.communicate()
    file_history_dict = {}
    for file_name in candidate_file_list:
        command = 'cmd /u /c git log --follow --all --pretty=format:\"%cd | %s\""-p '+file_name
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        result = p.communicate()[0]
        result = result.decode('utf-8',errors='ignore')
        lines = result.split("\n")
        change_date_list = []
        for line in lines:
            line = line.replace("\n","")
            if line.find("|") == -1:
                continue
            commit_date = line.split("|")[0].strip()
            commit_message= line.split("|")[1].strip()            
            if commit_message.find("fix")> -1 or commit_message.find("bug")> -1 or commit_message.find("issue")> -1 or commit_message.find("fail")> -1 or commit_message.find("error")> -1  or commit_message.find("#")> -1 :
                change_date_list.append(commit_date)

        file_history_list = []
        for change_date in change_date_list:
            change_date = ' '.join(change_date.split(" ")[1:-1])
            date_time_obj = datetime.datetime.strptime(change_date, "%b %d %H:%M:%S %Y")
            file_history_list.append(str(date_time_obj))
        file_history_dict[file_name] = file_history_list
    
    f = open(commits_path+"\\"+repo+".txt", "w", encoding="utf8")
    for file_name in file_history_dict.keys():
        commit_date = '|'.join(file_history_dict[file_name])
        f.write(file_name+"\t"+commit_date+"\n")
    f.close()
    print(repo, len(file_history_dict))
    
print(len(repos), target_bug_num)
                
