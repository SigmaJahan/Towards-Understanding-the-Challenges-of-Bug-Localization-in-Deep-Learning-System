# f.write(repo+"\t"+ver+"\t"+bug+"\t"+q_type+"\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")
                
checked_bugs = []
model_bug_num = {}
model_top1_dict = {}
model_top5_dict = {}
model_top10_dict = {}
model_mrr_dict = {}
model_map_dict = {}
lines = open("./results_rq4.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    tokens = line.split("\t")    
    identifier = tokens[0]+"_"+tokens[1]+"_"+tokens[2]+"_"+tokens[3]
    if identifier in checked_bugs:
        continue
    loc_type = tokens[3]
    top_rank = float(tokens[5])
    top1 = 0
    top5 = 0
    top10 = 0
    if top_rank <= 1.1:
        top1 += 1
    if top_rank <= 5.1:
        top5 += 1
    if top_rank <= 10.1:
        top10 += 1
    rr = float(tokens[6])
    ap = float(tokens[7])

    if loc_type not in model_bug_num.keys():
        model_bug_num[loc_type] = 0
        model_top1_dict[loc_type] = 0
        model_top5_dict[loc_type] = 0
        model_top10_dict[loc_type] = 0
        model_mrr_dict[loc_type] = 0
        model_map_dict[loc_type] = 0
    
    model_bug_num[loc_type] += 1
    model_top1_dict[loc_type] += top1
    model_top5_dict[loc_type] += top5
    model_top10_dict[loc_type] += top10
    model_mrr_dict[loc_type] += rr
    model_map_dict[loc_type] += ap


for key in model_bug_num.keys():
    bug_num = model_bug_num[key]
    top1 = model_top1_dict[key]
    top5 = model_top5_dict[key]
    top10 = model_top10_dict[key]
    mrr = model_mrr_dict[key]
    map = model_map_dict[key]
    print(key, bug_num, round(top1/bug_num,3), round(top5/bug_num,3), round(top10/bug_num,3), round(mrr/bug_num,3), round(map/bug_num,3))


