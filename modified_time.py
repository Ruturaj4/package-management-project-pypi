import requests
import json
from bs4 import BeautifulSoup

with open("all.json", "r") as f:
    all_packages = json.load(f)

packages = []

for package in all_packages:
    #print(package["package"])
    packages.append(package["package_name"])

packages = set(packages)

print(len(packages))

#Request pypu repository
url = "https://pypi.org/project/"

dic = {}

for package in packages:
    try:
        print(package)
        page = requests.get(url+str(package))
        soup = BeautifulSoup(page.content, 'html.parser')
        dic[package] = soup.find_all("p", class_="package-header__date")[0].find("time")["datetime"])
    except:
        pass

with open("modified_date.json", "w") as f:
    json.dump(dic, f)


