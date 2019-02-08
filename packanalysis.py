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
        # pick a key if the of the corresponding package
        if key in v:
            temp.append(k)
    # Save the package as a kwy and values as the violating or targetted packages
    mydic[key] = temp

print(len(mydic))

with open('importanal.json', 'w') as fp:
    json.dump(mydic, fp)
