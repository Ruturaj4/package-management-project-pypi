import json

with open("importanal.json", "r") as f:
    dic = json.load(f)

print(len(dic))
print(dic["beautifulsoup4"])
count = 0
for k,v in dic.items():
    if len(v) > 1:
        print(v)
        break

print(count)

for k,v in dic.copy().items():
    if len(v) < 2:
        del dic[k]
print(len(dic))
print(dic["bs4"])
