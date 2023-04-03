import os
import json
import datetime
import shutil
import subprocess
import ast

import os
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import humps
import string
import re
from camelsplit import camelsplit

stop_words = set(stopwords.words("english"))

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def remove_numbers(text):
    result = re.sub(r'\d+', '', text)
    return result

def remove_punctuation(text):    
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def remove_whitespace(text):
    return  " ".join(text.split())

def remove_stopwords(text):
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    filtered_text = [word for word in filtered_text if len(word) > 2]
    return ' '.join(filtered_text)

def convert_special_tags(text):
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", "\"")
    text = text.replace("&#39;", "\'")
    return text

def preprocess(text):
    text = convert_special_tags(text)
    text = cleanhtml(text)
    text = re.sub("[?|<|>|?|:|/|-|.|,|!|(|)|{|}|=|'|\"]", " ", text)
    text = remove_numbers(text)
    text = remove_whitespace(text)
    tokens = text.split()
    new_text = ""
    for token in tokens:
        if len(token) < 3:
            continue
        token = humps.camelize(token)
        new_text = new_text + token+" "
    text = new_text
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = remove_whitespace(text)
    new_text = ""
    for tokens in text.split():
        token = ' '.join(camelsplit(tokens))
        new_text = new_text + token+" "
        if token != tokens:
            new_text = new_text + tokens+" "
    text = remove_whitespace(new_text)
    text = text.lower()
    text = remove_stopwords(text)
    return text
    

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                file_list.append(full_filename)
    except PermissionError:
        pass


def hack_methods(codes, target_file_path, encoding_type):
    root = None
    try:
        data = open(target_file_path).read()
        root = ast.parse(data, target_file_path)
    except (UnicodeDecodeError, ValueError) as e:          
        data = open(target_file_path, encoding=encoding_type).read()
        root = ast.parse(data, target_file_path)


    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef):
            body_text = ""
            for body in node.body:
                start_line =body.lineno-1
                end_line =  body.end_lineno
                body_text = body_text + " "+' '.join(codes[start_line:end_line])
            yield node.name+"\t"+body_text

def hack_classes(codes, target_file_path, encoding_type):
    root = None
    try:
        data = open(target_file_path).read()
        root = ast.parse(data, target_file_path)
    except (UnicodeDecodeError, ValueError) as e:          
        data = open(target_file_path, encoding=encoding_type).read()
        root = ast.parse(data, target_file_path)

    for node in ast.walk(root):
        if isinstance(node, ast.ClassDef):
            class_text = ""
            class_text = class_text + "class " + node.name
            body_text = ""
            for body in node.body:
                if isinstance(body, ast.FunctionDef):
                    start_line = body.lineno-1
                    end_line = body.end_lineno
                    body_text = body_text + " " + ' '.join(codes[start_line:end_line])
            yield [node.name, class_text + ":\n" + body_text]

def hack_variables(target_file_path, encoding_type):
    root = None
    try:
        data = open(target_file_path).read()
        root = ast.parse(data, target_file_path)
    except (UnicodeDecodeError, ValueError) as e:          
        data = open(target_file_path, encoding=encoding_type).read()
        root = ast.parse(data, target_file_path)

    for node in ast.walk(root):
        if isinstance(node, ast.Assign):
            var_names = []
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_names.append(target.id)
            if var_names:
                var_value = ast.unparse(node.value).strip()
                yield f"{', '.join(var_names)} = {var_value}"

def hack_comments(target_file_path, encoding_type):
    root = None
    try:
        data = open(target_file_path).read()
        root = ast.parse(data, target_file_path)
    except (UnicodeDecodeError, ValueError) as e:          
        data = open(target_file_path, encoding=encoding_type).read()
        root = ast.parse(data, target_file_path)
        
    for node in ast.walk(root):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            yield node.value.s

def get_code_text(target_file_path):
    codes = []
    encoding_type = "cp949"
    try:
        codes = open(target_file_path, "r", encoding="utf8").readlines()
        encoding_type ="utf8"
    except UnicodeDecodeError:              
        try:
            codes = open(target_file_path, "r", encoding="euc-kr").readlines()
            encoding_type ="euc-kr"
        except UnicodeDecodeError:
            try:
                codes = open(target_file_path, "r", encoding="iso-8859-1").readlines()                              
                encoding_type ="iso-8859-1"
            except UnicodeDecodeError:
                codes = open(target_file_path, "r", encoding="cp949").readlines()
                encoding_type ="cp949"
    return codes, encoding_type

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

base_path = path_dict["searchspace_path"]
file_out_path = path_dict["file_path"]
function_out_path = path_dict["function_path"]
class_path = path_dict["class_path"]
variable_path = path_dict["variable_path"]
comment_path = path_dict["comment_path"]

# repos = os.listdir(base_path)
file_list = []
for repo in ['paddlepaddle+paddle', 'ray-project+ray', 'tensorflow+tensorflow', 'pytorch+fairseq', 'tensorpack+tensorpack', 'pytorch+ignite', 'opencv+opencv', 'pytorchlightning+pytorch-lightning', 'tensorflow+addons', 'tensorflow+tfjs']:
    vers = os.listdir(base_path+repo+"\\")
    for ver in vers:
        if os.path.exists(file_out_path+repo+"\\"+ver+"\\python\\") is True:
            continue
        prefix = base_path + repo+"\\"+ver+"\\"
        space_path = base_path + repo+"\\"+ver+"\\"
        file_list = []
        search(space_path)
        print(repo, ver, len(file_list))
 
        if os.path.exists(file_out_path+repo+"\\"+ver+"\\python\\") is False:
            os.makedirs(file_out_path+repo+"\\"+ver+"\\python\\")
            os.makedirs(file_out_path+repo+"\\"+ver+"\\python_pp\\")
        if os.path.exists(function_out_path+repo+"\\"+ver+"\\python\\") is False:
            os.makedirs(function_out_path+repo+"\\"+ver+"\\python\\")
            os.makedirs(function_out_path+repo+"\\"+ver+"\\python_pp\\")
        if os.path.exists(class_path+repo+"\\"+ver+"\\python\\") is False:
            os.makedirs(class_path+repo+"\\"+ver+"\\python\\")
            os.makedirs(class_path+repo+"\\"+ver+"\\python_pp\\")
        if os.path.exists(variable_path+repo+"\\"+ver+"\\python\\") is False:
            os.makedirs(variable_path+repo+"\\"+ver+"\\python\\")
            os.makedirs(variable_path+repo+"\\"+ver+"\\python_pp\\")
        if os.path.exists(comment_path+repo+"\\"+ver+"\\python\\") is False:
            os.makedirs(comment_path+repo+"\\"+ver+"\\python\\")
            os.makedirs(comment_path+repo+"\\"+ver+"\\python_pp\\")
            
        f_file = open(file_out_path+repo+"\\"+ver+"\\PythonKeyMap.txt","w",encoding="utf8")
        f_function = open(function_out_path+repo+"\\"+ver+"\\PythonKeyMap.txt","w",encoding="utf8")
        f_class = open(class_path+repo+"\\"+ver+"\\PythonKeyMap.txt","w",encoding="utf8")
        f_variables = open(variable_path+repo+"\\"+ver+"\\PythonKeyMap.txt","w",encoding="utf8")
        f_comments = open(comment_path+repo+"\\"+ver+"\\PythonKeyMap.txt","w",encoding="utf8")

        index_file = 0            
        index_function = 0
        index_class = 0            
        index_variable = 0
        index_comments = 0
        for file_name in file_list:
            if str(file_name).endswith(".py"):
                name = file_name.replace(prefix, "")
                output_file = file_out_path+repo+"\\"+ver+"\\python\\"+str(index_file)+".py"
                shutil.copyfile(file_name, output_file)
                f_file.write(str(index_file)+"|"+name+"\n")

                codes, encoding_type = get_code_text(output_file)

                file_writer = open(file_out_path+repo+"\\"+ver+"\\python_pp\\"+str(index_file)+".txt", "w", encoding="utf8")                
                file_writer.write(preprocess(' '.join(codes)))
                file_writer.close()


                methods = ""
                try:
                    methods = list(hack_methods(codes, output_file, encoding_type))
                    classes = list(hack_classes(codes, output_file, encoding_type))
                    variables = list(hack_variables(output_file, encoding_type))
                    comments = list(hack_comments(output_file, encoding_type))    
                except (SyntaxError, ValueError) as e:
                    print('error', output_file)             
                    index_file += 1
                    continue
                
                for method in methods:
                    method_writer = open(function_out_path+repo+"\\"+ver+"\\python\\"+str(index_function)+".txt", "w", encoding="utf8")
                    method_name = method.split("\t")[0]
                    method_writer.write(method_name+"\n")
                    method_body = method.split("\t",2)[1]
                    method_writer.write(method_body)
                    method_writer.close()
                    f_function.write(str(index_file)+"|"+name+"|"+str(index_function)+"|"+method_name+"\n")

                    pp_text = preprocess(method_name+" "+method_body)
                    pp_writer = open(function_out_path+repo+"\\"+ver+"\\python_pp\\"+str(index_function)+".txt", "w", encoding="utf8")
                    pp_writer.write(pp_text)
                    pp_writer.close()
                    index_function += 1
    
                for clazs in classes:
                    class_writer = open(class_path+repo+"\\"+ver+"\\python\\"+str(index_class)+".txt", "w", encoding="utf8")
                    class_writer.write(clazs[1])
                    class_writer.close()
                    f_class.write(str(index_file)+"|"+name+"|"+str(index_class)+"|"+clazs[0]+"\n")

                    pp_text = preprocess(clazs[0]+" "+clazs[1])
                    pp_writer = open(class_path+repo+"\\"+ver+"\\python_pp\\"+str(index_class)+".txt", "w", encoding="utf8")
                    pp_writer.write(pp_text)
                    pp_writer.close()
                    index_class += 1

                for variable in variables:
                    variable_writer = open(variable_path+repo+"\\"+ver+"\\python\\"+str(index_variable)+".txt", "w", encoding="utf8")
                    variable_writer.write(variable)
                    variable_writer.close()
                    f_variables.write(str(index_file)+"|"+name+"|"+str(index_variable)+"|"+variable+"\n")

                    pp_text = preprocess(variable)
                    pp_writer = open(variable_path+repo+"\\"+ver+"\\python_pp\\"+str(index_variable)+".txt", "w", encoding="utf8")
                    pp_writer.write(pp_text)
                    pp_writer.close()
                    index_variable += 1
                
                for comment in comments:
                    comment_writer = open(comment_path+repo+"\\"+ver+"\\python\\"+str(index_comments)+".txt", "w", encoding="utf8")
                    comment_writer.write(comment)
                    comment_writer.close()
                    f_comments.write(str(index_file)+"|"+name+"|"+str(index_comments)+"|"+comment+"\n")

                    pp_text = preprocess(comment)
                    pp_writer = open(comment_path+repo+"\\"+ver+"\\python_pp\\"+str(index_comments)+".txt", "w", encoding="utf8")
                    pp_writer.write(pp_text)
                    pp_writer.close()
                    index_comments += 1
                index_file += 1

        f_file.close()
        f_class.close()
        f_function.close()
        f_variables.close()
        f_comments.close()
