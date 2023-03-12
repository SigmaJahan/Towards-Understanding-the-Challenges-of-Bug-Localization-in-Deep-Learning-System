
# f.write(repo+"\t"+ver+"\t"+bug+"\tvsm\t"+str(len(gtfs))+"\t"+str(top_rank)+"\t"+str(rr)+"\t"+str(ap)+"\n")

checked_bugs = []   
model_bug_num = {}
model_top1_dict = {}
model_top5_dict = {}
model_top10_dict = {}
model_mrr_dict = {}
model_map_dict = {}
lines = open("./results_rq1.txt","r", encoding="utf8").readlines()
for line in lines:
    line = line.replace("\n","")
    tokens = line.split("\t")
    identifier = tokens[0]+"_"+tokens[1]+"_"+tokens[2]+"_"+tokens[3]
    if identifier in checked_bugs:
        continue
    checked_bugs.append(identifier)
    ir_model = tokens[3]
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

    if ir_model not in model_bug_num.keys():
        model_bug_num[ir_model] = 0
        model_top1_dict[ir_model] = 0
        model_top5_dict[ir_model] = 0
        model_top10_dict[ir_model] = 0
        model_mrr_dict[ir_model] = 0
        model_map_dict[ir_model] = 0
    
    model_bug_num[ir_model] += 1
    model_top1_dict[ir_model] += top1
    model_top5_dict[ir_model] += top5
    model_top10_dict[ir_model] += top10
    model_mrr_dict[ir_model] += rr
    model_map_dict[ir_model] += ap


for key in model_bug_num.keys():
    bug_num = model_bug_num[key]
    top1 = model_top1_dict[key]
    top5 = model_top5_dict[key]
    top10 = model_top10_dict[key]
    mrr = model_mrr_dict[key]
    map = model_map_dict[key]
    print(key, bug_num, round(top1/bug_num,3), round(top5/bug_num,3), round(top10/bug_num,3), round(mrr/bug_num,3), round(map/bug_num,3))


