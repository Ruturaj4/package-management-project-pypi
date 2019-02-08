# This is a file for temporary calcualtions

import json

with open("downloads_counts.json", "r") as f:
    dic = json.load(f)

print(len(dic))

for k,v in dic.items():
    dic[k] = int(v.replace(',', ''))
#print(dic)

sorted_dic = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
for p in sorted_dic[:1000]:
    if "beautifulsoup4" == p[0]:
        print(p)
        print(sorted_dic.index(p))

print(sorted_dic[:5])

with open("importanal.json", "r") as fb:
    ana = json.load(fb)

print(len(ana))

for k,v in ana.copy().items():
    if len(v) < 2:
        del ana[k]

print(len(ana))
#print({k: ana[k] for k in list(ana)[:5]})

li = set()

for p in sorted_dic:
    for k,v in ana.items():
        if p[0] == k:
            continue
        if p[0] in v:
            li.add(k)

if "bs4" in li:
    print("yes")

print(len(li))
