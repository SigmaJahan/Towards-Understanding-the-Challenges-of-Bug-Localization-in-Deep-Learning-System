import os
import subprocess
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

base_path = path_dict["git_path"]
tag_path = path_dict["tag_path"]
if os.path.exists(tag_path) is False:
    os.makedirs(tag_path)

repos = os.listdir(base_path)
for repo in repos:
    projects = os.listdir(base_path+repo)
    if len(projects) > 1:
        print('error #project > 1'+repo)
        break
    project = projects[0]

    if os.path.exists(tag_path+repo+".txt") is True:
        continue

    git_path = base_path + repo+"\\"+project+"\\"
    os.chdir(git_path)
    print(git_path)
    command = "git show-ref --tags"

    command = 'cmd /u /c '+command
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    result = p.communicate()[0]
    result = result.decode('utf-8',errors='ignore')
    lines = result.split("\n")
    f = open(tag_path+repo+".txt", "w", encoding="utf8")
    f.write('tag|commit|date|time\n')

    for line in lines:
        line = line.replace("\n","")
        if len(line.split(" ")) < 2:
            continue
        commit_id = line.split(" ")[0]       

        tag_tokens = line.split(" ")[1].split("/")        
        tag_name =tag_tokens[len(tag_tokens)-1]        
        if tag_name.find("doc") > -1:
            continue

        # noise cases in ml-agents
        if repo == "unity-technologies+ml-agents":
            if tag_name.find("com.") > -1 or tag_name.find("latest_") > -1 or tag_name.find("python") > -1:
                continue        
        # noise cases in pipcook
        if repo == "alibaba+pipcook":
            if tag_name.find("@") > -1:
                continue 
        # noise cases in allennlp
        if repo == "allenai+allennlp":
            if tag_name.startswith("v") is False:
                continue
        # noise cases in tfjs
        if repo == "tensorflow+tfjs":
            if tag_name.find("tfjs-react") > -1:
                continue
            if tag_name.find("tfjs-back") > -1:
                continue
            if tag_name.find("tfjs-tflite") > -1:
                continue
            if tag_name.find("tfjs-automl") > -1:
                continue
            if tag_name.find("tfjs-react") > -1:
                continue
            if tag_name.find("tfjs-vis") > -1:
                continue
            if tag_name.find("tfjs-node") > -1:
                continue
            if tag_name.find("tfjs-layers") > -1:
                continue
            if tag_name.find("tfjs-data") > -1:
                continue
            if tag_name.find("tfjs-converter") > -1:
                continue
            if tag_name.find("tfjs-converter") > -1:
                continue
            if tag_name.find("tfjs-core") > -1:
                continue
            if tag_name.find(".") == -1:
                continue
        # noise cases in pysyft
        if repo == "openmined+pysyft":
            if tag_name.startswith("hydrogen") is True:
                continue
        # noise cases in ml5-library
        if repo == "ml5js+ml5-library":
            if tag_name.lower().startswith("v") is False:
                continue
        # noise cases in vott
        if repo == "microsoft+vott":
            if tag_name.find(".") == -1:
                continue
        # noise cases in pai
        if repo == "microsoft+pai":
            if tag_name.startswith("v") is False:
                continue
        # noise cases in onnxruntime
        if repo == "microsoft+onnxruntime":
            if tag_name.startswith("v") is False:
                continue
        # noise cases in nlp-recipes
        if repo == "microsoft+nlp-recipes":
            if tag_name.find("BEFORE_REMOVING_SANNETWORK_22JAN20") > -1:
                continue
        # noise cases in deepspeed
        if repo == "microsoft+deepspeed":
            if tag_name.find("grad-norm-test") > -1:
                continue
        # noise cases in cntk
        if repo == "microsoft+cntk":
            if tag_name.find("gtc201705") > -1:
                continue
            if tag_name.find("CNTKCustomMKL") > -1:
                continue
            if tag_name.find("onnx1.0") > -1:
                continue
        # noise cases in distiller
        if repo == "intellabs+distiller":
            if tag_name.startswith("v") is False:
                continue

        command = 'cmd /u /c '+'git show -s --format=%ci '+commit_id
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        result = p.communicate()[0]
        tokens = result.decode('utf-8',errors='ignore').split("\n")   
        commit_datetime = tokens[len(tokens)-2]
        commit_date = commit_datetime.split(" ")[0]
        commit_time = commit_datetime.split(" ")[1]
        print(repo, tag_name, commit_id, commit_date, commit_time)

        try:
            date_time_str = commit_date+" "+commit_time+".0"
            date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        except:
            tokens = (' '.join(tokens)).split("]")
            commit_datetime = tokens[1]
            commit_date = commit_datetime.split(" ")[0]
            commit_time = commit_datetime.split(" ")[1]
            print(repo, tag_name, commit_id, commit_date, commit_time)
            try:
                date_time_str = commit_date+" "+commit_time+".0"
                date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
            except:
                tokens = result.decode('utf-8',errors='ignore').split("\n")   
                tokens = (' '.join(tokens)).split(")")
                try:
                    commit_datetime = tokens[2]
                    commit_date = commit_datetime.split(" ")[0]
                    commit_time = commit_datetime.split(" ")[1]
                    print(repo, tag_name, commit_id, commit_date, commit_time)
                except:
                    tokens = result.decode('utf-8',errors='ignore').split("\n")   
                    tokens = (' '.join(tokens)).split(")")
                    commit_datetime = tokens[1]
                    commit_date = commit_datetime.split(" ")[0]
                    commit_time = commit_datetime.split(" ")[1]
                    print(repo, tag_name, commit_id, commit_date, commit_time)
        
        f.write(tag_name+"|"+commit_id+"|"+commit_date+"|"+commit_time+"\n")
    f.close()



    