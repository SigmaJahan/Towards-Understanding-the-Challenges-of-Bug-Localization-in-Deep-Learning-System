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
nltk.download('stopwords')
nltk.download('punkt')

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

 
bug_path = path_dict["bug_path"]
output_path = path_dict["query_path"]
if os.path.exists(output_path) is False:
    os.makedirs(output_path)


denchmark_start_tag_r = re.compile('<denchmark(.*?)>')
denchmark_end_tag_r = re.compile('</denchmark(.*?)>')
pStrackRegex = re.compile("Traceback[\s\S]+?(?=^\[|\Z|Error:|\?)")
errorRegex = re.compile("((.*?).Error)")
exceptRegex = re.compile("((.*?).Exception)")
blizzard_CE_path = path_dict["blz_ce_path"]

repos = os.listdir(bug_path)
buggy_file_type = {}
all_bug_num = 0
bug_num_dict = {}
for repo in repos:
    versions = os.listdir(bug_path+repo+"\\")
    for version in versions:
        bugs = os.listdir(bug_path+repo+"\\"+version+"\\")
        for bug in bugs:
            all_bug_num+= 1
            bug_id = bug.replace(".json","")

            if os.path.exists(output_path+repo+"\\"+version+"\\"+bug_id+"\\") is False:
                os.makedirs(output_path+repo+"\\"+version+"\\"+bug_id+"\\")

            br_path = bug_path+repo+"\\"+version+"\\"+bug            
            contents = None
            with open(br_path, 'r', encoding ="utf8") as j:
                contents = json.loads(j.read())
                bug_report = contents['BR']['BR_text']
                summary = bug_report['BRsummary']
                desc_w_tag = str(bug_report['BRdescription'])
                comments = contents['BR']['comments']
                comments_text = ""

                # 1.1. BASE-Summary
                f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_base-sum.txt", "w", encoding="utf8")
                f.write(summary)
                f.close()
                query_summary = preprocess(summary)
                f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_base-sum.txt", "w", encoding="utf8")
                f.write(query_summary)
                f.close()
                
                # 1.2. BASE-Description
                desc_wo_tags = desc_w_tag
                f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_base-desc_html.txt", "w", encoding="utf8")
                f.write(desc_w_tag)
                f.close()  

                find_tags = denchmark_start_tag_r.findall(desc_wo_tags)
                find_tags += denchmark_end_tag_r.findall(desc_wo_tags)
                for find_tag in find_tags:
                    desc_wo_tags = desc_wo_tags.replace("<denchmark"+find_tag+">","")
                    desc_wo_tags = desc_wo_tags.replace("</denchmark"+find_tag+">","")
                f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_base-desc.txt", "w", encoding="utf8")
                f.write(desc_wo_tags)
                f.close()                
                query_desc_wo_tags = preprocess(desc_wo_tags)
                f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_base-desc.txt", "w", encoding="utf8")
                f.write(query_desc_wo_tags)
                f.close()
                    

                data_nl_query = " "+query_summary+" "+query_desc_wo_tags+" "
                # 2.1. DATA-Strace
                desc_strace = desc_wo_tags                                                                                                   
                groups =  pStrackRegex.search(desc_wo_tags)
                pstrace_text = ""
                if groups != None:
                    pstrace_text = groups.group() 

                if len(pstrace_text) > 3:                   
                    if "data-strace" not in bug_num_dict.keys():
                        bug_num_dict["data-strace"] = 0
                    bug_num_dict["data-strace"] += 1

                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_data-strace.txt", "w", encoding="utf8")
                    f.write(pstrace_text+"\n")
                    f.close()                    
                    pp_trace = preprocess(pstrace_text)
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_data-strace.txt", "w", encoding="utf8")
                    f.write(pp_trace)
                    f.close()
                    for token in pp_trace.split(" "):
                        data_nl_query = data_nl_query.replace(" "+token+" "," ", 1)
                                
                # 2.2. DATA-ErrMessage
                desc_strace = desc_wo_tags
                error_msg_text = ""
                errors = errorRegex.findall(desc_strace)
                for error_msg in errors:
                    for msg in error_msg:
                        error_msg_text = error_msg_text + msg.replace("\n"," ")+"\n"
                        break
                errors = exceptRegex.findall(desc_strace)
                for error_msg in errors:
                    for msg in error_msg:
                        error_msg_text = error_msg_text + msg.replace("\n"," ")+"\n"
                        break    
                if len(error_msg_text) > 3:                    
                    if "data-errmsg" not in bug_num_dict.keys():
                        bug_num_dict["data-errmsg"] = 0
                    bug_num_dict["data-errmsg"] += 1

                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_data-errmsg.txt", "w", encoding="utf8")
                    f.write(error_msg_text+"\n")
                    f.close()                    
                    pp_err = preprocess(error_msg_text)
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_data-errmsg.txt", "w", encoding="utf8")
                    f.write(pp_err+"\n")
                    f.close()                    
                    for token in pp_err.split(" "):
                        data_nl_query = data_nl_query.replace(" "+token+" "," ", 1)
                
                # 2.3. DATA-CE
                # It is should be performed after extracting CE tokens by BLIZZARD tool
                ce_path = blizzard_CE_path+repo+"\\"+version+"\\"+bug_id+"\\raw_pe_terms.txt"
                if os.path.exists(ce_path) is True:
                    lines = open(ce_path, "r", encoding="utf8").readlines()
                    ce_text = ""
                    for line in lines:
                        line = line.replace("\n"," ")
                        ce_text = ce_text + line
                    if len(ce_text) > 3:
                        if "data-ce" not in bug_num_dict.keys():
                            bug_num_dict["data-ce"] = 0
                        bug_num_dict["data-ce"] += 1

                        f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_data-ce.txt", "w", encoding="utf8")
                        f.write(ce_text+"\n")
                        f.close()                        

                        pp_ce = preprocess(ce_text)
                        f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_data-ce.txt", "w", encoding="utf8")
                        f.write(pp_ce+"\n")
                        f.close()
                        
                        for token in pp_ce.split(" "):
                            data_nl_query = data_nl_query.replace(" "+token+" "," ", 1)
                
                # 2.4. DATA-NL
                if len(data_nl_query) > 3:                    
                    if "data-nl" not in bug_num_dict.keys():
                        bug_num_dict["data-nl"] = 0
                    bug_num_dict["data-nl"] += 1
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_data-nl.txt", "w", encoding="utf8")
                    f.write(data_nl_query+"\n")
                    f.close()



                tag_nl_query = " "+query_summary+" "+query_desc_wo_tags+" "
                # 3.1. TAG-CODE
                desc_code = desc_w_tag
                codes_tokens = desc_code.split("<denchmark-code>")
                codes_text = ""    
                for codes_token in codes_tokens:
                    if codes_token.find("</denchmark-code>") == -1:
                        continue
                    end_token = codes_token.split("</denchmark-code>")[0]
                    codes_text = codes_text + end_token.replace("\n"," ")+"\n"
                if len(codes_text) > 3:                                   
                    if "tag-code" not in bug_num_dict.keys():
                        bug_num_dict["tag-code"] = 0
                    bug_num_dict["tag-code"] += 1
                    
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_tag-code.txt", "w", encoding="utf8")
                    f.write(codes_text)
                    f.close()

                    query_raw_code_tagged = preprocess(codes_text)
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_tag-code.txt", "w", encoding="utf8")
                    f.write(query_raw_code_tagged)
                    f.close()
                    for token in query_raw_code_tagged.split(" "):
                        tag_nl_query = tag_nl_query.replace(" "+token+" "," ", 1)
                                                    

                # 3.2. TAG-LINK
                desc_code = desc_w_tag
                links_tokens = desc_code.split("<denchmark-link:")
                links_text = ""    
                for links_token in links_tokens:
                    if links_token.find("</denchmark-link") == -1:
                        continue
                    end_token = links_token.split("</denchmark-link")[0].split(">")[1]
                    links_text = links_text + end_token.replace("\n"," ")+"\n"
                if len(links_text) > 3:                                   
                    if "tag-link" not in bug_num_dict.keys():
                        bug_num_dict["tag-link"] = 0
                    bug_num_dict["tag-link"] += 1                    
                    
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_tag-link.txt", "w", encoding="utf8")
                    f.write(links_text)
                    f.close()

                    query_raw_link_tagged = preprocess(links_text)
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_tag-link.txt", "w", encoding="utf8")
                    f.write(query_raw_link_tagged)
                    f.close()
                    for token in query_raw_link_tagged.split(" "):
                        tag_nl_query = tag_nl_query.replace(" "+token+" "," ", 1)

                
                # 3.3. TAG-HEADER
                desc_code = desc_w_tag
                header_tokens = desc_code.split("<denchmark-h")
                headers_text = ""    
                for headers_token in header_tokens:
                    if headers_token.find("</denchmark-h") == -1:
                        continue
                    end_token = headers_token.split("</denchmark-h")[0].split(">")[1]
                    headers_text = headers_text + end_token.replace("\n"," ")+"\n"
                if len(headers_text) > 3:    
                             
                    if "tag-header" not in bug_num_dict.keys():
                        bug_num_dict["tag-header"] = 0
                    bug_num_dict["tag-header"] += 1

                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\raw_tag-header.txt", "w", encoding="utf8")
                    f.write(headers_text)
                    f.close()

                    query_raw_header_tagged = preprocess(headers_text)
                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_tag-header.txt", "w", encoding="utf8")
                    f.write(query_raw_header_tagged)
                    f.close()
                    for token in query_raw_header_tagged.split(" "):
                        tag_nl_query = tag_nl_query.replace(" "+token+" "," ", 1)

                # 3.4. TAG- NL
                if len(tag_nl_query) > 3:                    
                    if "tag-nl" not in bug_num_dict.keys():
                        bug_num_dict["tag-nl"] = 0
                    bug_num_dict["tag-nl"] += 1

                    f = open(output_path+repo+"\\"+version+"\\"+bug_id+"\\query_tag-nl.txt", "w", encoding="utf8")
                    f.write(tag_nl_query+"\n")
                    f.close()

    print(repo, all_bug_num, end="\t")
    for key in bug_num_dict.keys():
        print(key+":",bug_num_dict[key], end="\t")
    print("\n")
                            