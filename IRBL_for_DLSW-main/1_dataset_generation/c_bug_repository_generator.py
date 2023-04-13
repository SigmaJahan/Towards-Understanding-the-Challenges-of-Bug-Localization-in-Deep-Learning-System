import os
import json
import datetime
import shutil


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

bugs_path = path_dict["denchmark_path"] + "\\JSonSet\\simplejson\\"
tag_path = path_dict["tag_path"]
output_path = path_dict["bug_path"]
if os.path.exists(output_path) is False:
    os.makedirs(output_path)

repos = os.listdir(bugs_path)
all_bug_num = 0
ver_bug_num = 0
for repo in repos:
    tag_file = tag_path + repo + ".txt"
    f = open(tag_file, "r", encoding="utf8")
    lines = f.readlines()[1:]
    tag_date_dict = {}
    commit_ids = []
    for line in lines:
        print(line)
        line = line.replace("\n", "")
        tag = line.split("|")[0]
        commit_id = line.split("|")[1]
        if commit_id in commit_ids:
            continue
        tag_date = line.split("|")[2]
        tag_time = line.split("|")[3]
        if not tag_date:
            continue

        commit_ids.append(commit_id)

        
        date_time_str = tag_date + " " + tag_time + ".0"
        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
        tag_date_dict[tag] = date_time_obj

    buggy_versions = set()
    version_bug_dict = {}
    bugs = os.listdir(bugs_path + repo + "\\")
    for bug in bugs:
        all_bug_num += 1

        bug_path = bugs_path + repo + "\\" + bug

        contents = None
        with open(bug_path, 'r', encoding="utf8") as j:
            contents = json.loads(j.read())

        reporting_datetime = contents['BR']['BRopenT']
        reporting_date = reporting_datetime.split("T")[0]
        reporting_time = reporting_datetime.split("T")[1].replace("Z", "")

        date_time_str = reporting_date + " " + reporting_time + ".0"
        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")

        prev_date = None
        prev_tag = None
        for tag_name in tag_date_dict.keys():
            tag_date = tag_date_dict[tag_name]
            if date_time_obj > tag_date:
                if prev_tag is None:
                    prev_tag = tag_name
                    prev_date = tag_date
                else:
                    if prev_date < tag_date:
                        prev_tag = tag_name
                        prev_date = tag_date

        if prev_tag is None:
            continue
        if prev_tag not in version_bug_dict.keys():
            version_bug_dict[prev_tag] = []
        version_bug_dict[prev_tag].append(bug)
        buggy_versions.add(prev_tag)
      

    for buggy_version in buggy_versions:
        bug_ids = version_bug_dict[buggy_version]
        bug_output_path = output_path + repo + "\\" + buggy_version + "\\"
        if os.path.exists(bug_output_path) is False:
            os.makedirs(bug_output_path)

        for bug_id in bug_ids:
            ver_bug_num += 1
            original_bug_path = bugs_path + repo + "\\" + bug_id
            new_bug_path = bug_output_path + bug_id
            shutil.copyfile(original_bug_path, new_bug_path)
        print(repo, buggy_version, len(bug_ids))

print(all_bug_num, ver_bug_num)