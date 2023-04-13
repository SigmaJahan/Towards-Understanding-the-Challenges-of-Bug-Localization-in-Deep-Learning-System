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


bugs_path = path_dict["bug_path"]
gtfs_path = path_dict["gtf_path"]
repos = os.listdir(bugs_path)
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
        if os.path.exists(gtfs_path+repo+"\\"+version+"\\") is False:
            os.makedirs(gtfs_path+repo+"\\"+version+"\\")
        bugs = os.listdir(bugs_path+repo+"\\"+version+"\\")
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
        
        for bug in bugs:                      
            bug_path = bugs_path+repo+"\\"+version+"\\"+bug
            contents = None
            with open(bug_path, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())
            
            bug_id = bug.replace(".json","")
            changed_files = contents['commit']['changed_files']
            file_type_set = set()            
            buggy_methods_ids = set()
            buggy_classes_ids = set()
            buggy_variables_ids = set()
            buggy_comments_ids = set()
            for changed_file in changed_files:

                change_type = contents['commit']['changed_files'][changed_file]['file_change_type']
                if change_type != "MODIFY":
                    continue
                original_file_name = contents['commit']['changed_files'][changed_file]['file_old_name'].lower()
                new_file_name = contents['commit']['changed_files'][changed_file]['file_new_name'].lower()

                if original_file_name not in files_name_set:
                    continue
                hunks =  contents['commit']['changed_files'][changed_file]["hunks"]
                for hunk in hunks:
                    isMethod = contents['commit']['changed_files'][changed_file]["hunks"][hunk]["Ismethod"]
                    if isMethod == 1:
                        method_name = contents['commit']['changed_files'][changed_file]["hunks"][hunk]["method_info"]["method_name"].lower()
                        method_identifier = original_file_name+"|"+method_name        
                        if method_identifier in methods_name_set:
                            buggy_methods_ids.add(methods_dict_by_name[method_identifier].split("|")[1])

                # Iterate over the files_dict
                for file_id in files_dict:
                    if files_dict[file_id] == original_file_name:
                        file_index = file_id
                        break
                    if files_dict[file_id] == new_file_name:
                        file_index = file_id
                        break

                # Open the keymap for class
                class_keymap_file = open (class_path, "r", encoding="utf8")
                lines = class_keymap_file.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    if line.find("|") == -1:
                        continue
                    tokens = line.split("|")
                    if tokens[0] == file_index:
                        buggy_classes_ids.add(tokens[-2])
                class_keymap_file.close()

                # Open the keymap for variable
                variable_keymap_file = open (variable_path, "r", encoding="utf8")
                lines = variable_keymap_file.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    if line.find("|") == -1:
                        continue
                    tokens = line.split("|")
                    if tokens[0] == file_index:
                        buggy_variables_ids.add(tokens[-2])
                variable_keymap_file.close()

                # Open the keymap for comment
                comment_keymap_file = open (comment_path, "r", encoding="utf8")
                lines = comment_keymap_file.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    if line.find("|") == -1:
                        continue
                    tokens = line.split("|")
                    if tokens[0] == file_index:
                        buggy_comments_ids.add(tokens[-2])
                comment_keymap_file.close()

            print(bug_id, buggy_methods_ids)
            print(repo, version, bug, buggy_methods_ids)
            if len(buggy_methods_ids) == 0:
                continue
            f = open(gtfs_path+repo+"\\"+version+"\\"+bug_id+"_method.txt", "w", encoding="utf8")
            for buggy_mth_id in buggy_methods_ids:
                f.write("python-"+buggy_mth_id+"\n")
            f = open(gtfs_path+repo+"\\"+version+"\\"+bug_id+"_class.txt", "w", encoding="utf8")
            for buggy_cls_id in buggy_classes_ids:
                f.write("python-"+buggy_cls_id+"\n")
            f = open(gtfs_path+repo+"\\"+version+"\\"+bug_id+"_variable.txt", "w", encoding="utf8")
            for buggy_var_id in buggy_variables_ids:
                f.write("python-"+buggy_var_id+"\n")
            f = open(gtfs_path+repo+"\\"+version+"\\"+bug_id+"_comment.txt", "w", encoding="utf8")
            for buggy_cmt_id in buggy_comments_ids:
                f.write("python-"+buggy_cmt_id+"\n")
            f.close()
            target_bug_num += 1
            project_bug_num += 1
    if project_bug_num > 0:
        target_repo_num += 1
print(target_repo_num, target_bug_num,project_bug_num)


