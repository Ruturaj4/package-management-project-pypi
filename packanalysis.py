import json

with open("packinfo.json", "r") as f:
    dic = json.load(f)

# To store packages to blame
mydic = {}

"""
# Removing values with egg-info in it
for k,v in dic.items():
    for value in v:
        if "egg-info" in value:
            v.remove(value)
"""

# Iterate through all saved packages
for key in dic:
    temp = []
    print(key)
    for k,v in dic.items():
        if key in v:
            temp.append(k)
    mydic[key] = temp

print(len(mydic))

with open('importanal.json', 'w') as fp:
    json.dump(mydic, fp)
