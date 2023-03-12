
lines = open("./z_header_info.txt","r", encoding="utf8").readlines()
header_dict = {}
for line in lines:
    line = line.replace("\n","")
    header_type = line.split("\t")[1]
    if header_type not in header_dict.keys():
        header_dict[header_type] =0 
    header_dict[header_type] += 1

for key in header_dict.keys():
    print(key, header_dict[key])

