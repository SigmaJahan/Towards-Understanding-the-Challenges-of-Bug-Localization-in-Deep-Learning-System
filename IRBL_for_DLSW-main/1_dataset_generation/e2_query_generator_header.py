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

query_path = path_dict["query_path"]

load_header_info = {}
lines = open("./z_header_info.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    header = line.split("\t")[0]
    info_type = line.split("\t")[1]
    load_header_info[header] = info_type

repos = os.listdir(query_path)
for repo in repos:
    vers = os.listdir(query_path+"\\"+repo+"\\")
    for ver in vers:
        bugs = os.listdir(query_path+"\\"+repo+"\\"+ver+"\\")
        for bug in bugs:
            contents = ' '.join(open(query_path+"\\"+repo+"\\"+ver+"\\"+bug+"\\raw_base-desc_html.txt","r", encoding="utf8").readlines()).replace("\n"," ")

            section_text = {}
            header_tokens = contents.split("<denchmark-h")            
            if len(header_tokens) > 1:
                print(repo+"\\"+ver+"\\"+bug, len(header_tokens))
                for header_token in header_tokens:
                    if header_token.find("</denchmark-h") > -1:
                        end_token = header_token.split("</denchmark-h")[0].split(">")[1]
                        contents = header_token.split("</denchmark-h")[1]
                        header_text = end_token.replace("\n"," ").replace("\t","")
                        if header_text in load_header_info.keys():
                            info_type = load_header_info[header_text]
                            if info_type not in section_text:
                                section_text[info_type] = ""
                            section_text[info_type] = section_text[info_type] + contents
                        else:
                            print(header_text)
                            info_type = "EXTRA"
                            if info_type not in section_text:
                                section_text[info_type] = ""
                            section_text[info_type] = section_text[info_type] + contents
                            

            for key in section_text.keys():
                info_type = key
                contents = section_text[info_type]
                writer = open(query_path+"\\"+repo+"\\"+ver+"\\"+bug+"\\raw_info-"+info_type+".txt", "w", encoding="utf8")
                writer.write(contents)
                writer.close()

                pp_contents = preprocess(contents)
                writer = open(query_path+"\\"+repo+"\\"+ver+"\\"+bug+"\\query_info-"+info_type+".txt", "w", encoding="utf8")
                writer.write(pp_contents)
                writer.close()

                


                