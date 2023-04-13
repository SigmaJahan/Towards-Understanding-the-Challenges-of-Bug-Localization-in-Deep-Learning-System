import os
import json
import datetime
import shutil
import subprocess
import re


def loader():
    path_dict = {}
    lines = open("./z_config.txt", "r", encoding="utf8").readlines()
    for line in lines:
        line = line.replace("\n", "")
        tokens = line.split("=", 2)
        label = tokens[0]
        path = tokens[1]
        path_dict[label] = path
    return path_dict


path_dict = loader()

base_path = path_dict["git_path"]
tag_path = path_dict["tag_path"]
bug_path = path_dict["bug_path"]
output_path = path_dict["searchspace_path"]

if os.path.exists(output_path) is False:
    os.makedirs(output_path)
#for specfic project
for repo in ['paddlepaddle+paddle', 'ray-project+ray', 'tensorflow+tensorflow', 'pytorch+fairseq', 'tensorpack+tensorpack', 'pytorch+ignite', 'opencv+opencv', 'pytorchlightning+pytorch-lightning', 'tensorflow+addons', 'tensorflow+tfjs']:
    projects = os.listdir(base_path + repo)
    if len(projects) > 1:
        print('error #project > 1' + repo)
        break
    project = projects[0]
    git_path = base_path + repo + "\\" + project + "\\"

    f = open(tag_path + repo + ".txt", "r", encoding="utf8")
    lines = f.readlines()[1:]
    ver_commit_dict = {}
    for line in lines:
        version = line.split("|")[0]
        commit_id = line.split("|")[1]
        ver_commit_dict[version] = commit_id

    versions = os.listdir(bug_path + repo + "\\")
    for version in versions:
        commit_id = ver_commit_dict[version]
        if os.path.exists(output_path + repo + "\\" + version + "\\") is True:
            continue
        os.makedirs(output_path + repo + "\\" + version + "\\")
        print(repo, version, commit_id)
        os.chdir(git_path)
        p = subprocess.Popen("cmd /u /c git checkout master --force", stdout=subprocess.PIPE)
        result = p.communicate()
        p = subprocess.Popen("cmd /u /c git checkout " + commit_id + " --force", stdout=subprocess.PIPE)
        result = p.communicate()
        print(result)
        output_base_path = output_path + repo + "\\" + version + "\\"
        dir_files = os.listdir(git_path)
        for dir_file in dir_files:
            if dir_file == ".git" or dir_file == ".github":
                continue
            elif os.path.isdir(git_path + "\\" + dir_file) is True:

                git_path = re.sub("\\\\\\\\", "\\\\", git_path)
                dir_file = re.sub("\\\\\\\\", "\\\\", dir_file)
                output_base_path = re.sub("\\\\\\\\", "\\\\", output_base_path)
                try:
                    shutil.copytree(git_path + "\\" + dir_file, output_base_path + "\\" + dir_file)
                except shutil.Error as exc:
                    errors = exc.args[0]
                    for error in errors:
                        print(error)

            else:

                git_path = re.sub("\\\\\\\\", "\\\\", git_path)
                dir_file = re.sub("\\\\\\\\", "\\\\", dir_file)
                output_base_path = re.sub("\\\\\\\\", "\\\\", output_base_path)

                try:
                    shutil.copy(git_path + "\\" + dir_file, output_base_path + "\\" + dir_file)
                except shutil.Error as exc:
                    errors = exc.args[0]
                    for error in errors:
                        print(error)