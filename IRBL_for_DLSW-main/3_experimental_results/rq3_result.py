strace_bugs = set()
lines = open("./results_rq2.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    tokens = line.split("\t")    
    identifier = tokens[0]+"_"+tokens[1]+"_"+tokens[2]
    q_type = tokens[3].replace(".txt","")
    if q_type.lower().find("trace") > -1:
        strace_bugs.add(identifier)

# f.write('\t'.join(weights_str)+"\t"+str(k_days_value[k_day])+"\t"+repo+"\t"+ver+"\t"+bug+"\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
import random      
model_bug_num = {}
model_top1_dict = {}
model_top5_dict = {}
model_top10_dict = {}
model_mrr_dict = {}
model_map_dict = {}
model_performance_dict = {}


lines = open("./results_rq3.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")    
    tokens = line.split("\t")   
    identifier = tokens[6]+"_"+tokens[7]+"_"+tokens[8]   
    # if identifier not in strace_bugs:
    #     continue

    weights = ' '.join(tokens[:6]) #(+kday)
    top_rank = float(tokens[-3])
    top1 = 0
    top5 = 0
    top10 = 0
    if top_rank <= 1.1:
        top1 += 1
    if top_rank <= 5.1:
        top5 += 1
    if top_rank <= 10.1:
        top10 += 1
    rr = float(tokens[-2])
    ap = float(tokens[-1])

    if weights not in model_bug_num.keys():
        model_bug_num[weights] = 0
        model_top1_dict[weights] = 0
        model_top5_dict[weights] = 0
        model_top10_dict[weights] = 0
        model_mrr_dict[weights] = 0
        model_map_dict[weights] = 0
        model_performance_dict[weights] = 0
    
    model_bug_num[weights] += 1
    model_top1_dict[weights] += top1
    model_top5_dict[weights] += top5
    model_top10_dict[weights] += top10
    model_mrr_dict[weights] += rr
    model_map_dict[weights] += ap
    model_performance_dict[weights] += (rr+ap)


scores_sort = sorted(model_performance_dict.items(), reverse=True, key=lambda item: item[1])
                                 
for key, score in scores_sort:    
    bug_num = model_bug_num[key]
    top1 = model_top1_dict[key]
    top5 = model_top5_dict[key]
    top10 = model_top10_dict[key]
    mrr = model_mrr_dict[key]
    map = model_map_dict[key]
    print(key,bug_num, round(top1/bug_num,3), round(top5/bug_num,3), round(top10/bug_num,3), round(mrr/bug_num,3), round(map/bug_num,3))


key = "0.0 0.0 0.0 0.0 1.0 60"  
bug_num = model_bug_num[key]
top1 = model_top1_dict[key]
top5 = model_top5_dict[key]
top10 = model_top10_dict[key]
mrr = model_mrr_dict[key]
map = model_map_dict[key]
print(key,bug_num, round(top1/bug_num,3), round(top5/bug_num,3), round(top10/bug_num,3), round(mrr/bug_num,3), round(map/bug_num,3))


