import statistics
import os

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

target_bug_set = {}
lines = open("./results_rq1.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    tokens = line.split("\t")    
    repo = tokens[0]
    ver = tokens[1]
    bug_id = tokens[2]
    gtf_num = tokens[4]
    if repo not in target_bug_set.keys():
        target_bug_set[repo] = {}
    if ver not in target_bug_set[repo].keys():
        target_bug_set[repo][ver] = set()
    target_bug_set[repo][ver].add(bug_id+"|"+gtf_num)

repo_num = 0
ver_num_list = []
file_num_list = []
bug_num = 0
gtf_list = []
for repo in target_bug_set.keys():
    repo_num += 1
    ver_num_list.append(len(target_bug_set[repo]))
    for ver in target_bug_set[repo].keys():
        file_path = files_path+repo+"\\"+ver+"\\python\\"
        files = os.listdir(file_path)
        file_num_list.append(len(files))
        bug_list = target_bug_set[repo][ver]
        for bug in bug_list:
            bug_num += 1
            bug_id = bug.split("|")[0]
            gtf_num = float(bug.split("|")[1])
            gtf_list.append(gtf_num)


print('file', repo_num, bug_num, round(statistics.mean(ver_num_list),1), max(ver_num_list), \
   round(statistics.mean(file_num_list),1), max(file_num_list), round(statistics.mean(gtf_list),1), max(gtf_list))



func_path = path_dict["function_path"]

target_bug_set = {}
lines = open("./results_rq4.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    tokens = line.split("\t")    
    repo = tokens[0]
    ver = tokens[1]
    bug_id = tokens[2]
    gtf_num = tokens[4]
    if repo not in target_bug_set.keys():
        target_bug_set[repo] = {}
    if ver not in target_bug_set[repo].keys():
        target_bug_set[repo][ver] = set()
    target_bug_set[repo][ver].add(bug_id+"|"+gtf_num)

repo_num = 0
ver_num_list = []
func_num_list = []
bug_num = 0
gtf_list = []
for repo in target_bug_set.keys():
    repo_num += 1
    ver_num_list.append(len(target_bug_set[repo]))
    for ver in target_bug_set[repo].keys():
        functions_path = func_path+repo+"\\"+ver+"\\python\\"
        func_files = os.listdir(functions_path)
        func_num_list.append(len(func_files))
        bug_list = target_bug_set[repo][ver]
        for bug in bug_list:
            bug_num += 1
            bug_id = bug.split("|")[0]
            gtf_num = float(bug.split("|")[1])
            gtf_list.append(gtf_num)
            # if len(gtf_list) == 638:
            #     print(repo, ver, bug, gtf_list)
        

print('function', repo_num, bug_num, round(statistics.mean(ver_num_list),1), max(ver_num_list), \
   round(statistics.mean(func_num_list),1), max(func_num_list), round(statistics.mean(gtf_list),1), max(gtf_list))