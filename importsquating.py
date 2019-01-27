import json

with open("importanal.json", "r") as f:
    dic = json.load(f)

print(len(dic))

for k,v in dic.copy().items():
    if len(v) < 2:
        del dic[k]
print(len(dic))
print(dic["bs4"])
