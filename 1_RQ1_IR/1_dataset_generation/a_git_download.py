import os
import subprocess

def cmd(command):
    command = 'cmd /u /c '+command
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    result = p.communicate()
    text = result[0]
    text = text.decode('utf-8',errors='ignore')    
    if len(text)>1:
        return text.split('\n')
    else:
        return []

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
denchmark_path = path_dict["denchmark_path"]
output_path =  path_dict["git_path"]

repos = os.listdir(denchmark_path+"JSonSet\\Fulljson\\")

git_url = "https://github.com/"

for repo in repos:
    user = repo.split("+")[0]
    project = repo.split("+")[1]

    repo_url = git_url + user+"/"+project
    output = output_path+user+"+"+project
    if os.path.exists(output) is False:
        os.makedirs(output)

    os.chdir(output)
    command = "git clone "+repo_url    
    print(command)
    cmd(command)

