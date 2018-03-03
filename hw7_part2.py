# 507/206 Homework 7 Part 2
import json

count = 0
#### Your Part 2 solution goes here ####
with open("directory_dict.json",'r') as load_f:
    umsi_titles = json.load(load_f)
for k,v in umsi_titles.items():
    if v["title"] == "PhD student":
        count += 1

#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
