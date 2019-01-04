import json
import requests
import bs4
from collections import OrderedDict

url = "https://pepy.tech/project/"

def download_counts():
    with open("all.json", "r") as f:
        pack = json.load(f)

    # A dictionary to store dowload counts for all the packages
    dic = {}
    #count = 0
    packages = []
    for item in pack:
        packages.append(item["package_name"])
    packages = list(OrderedDict.fromkeys(packages))
    for item in packages:
        #count += 1
        print(item)
        try:
            res = requests.get(url + item)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            # td is the tag they used. And taking 1st element from that
            td = soup.findAll("td")
            print(td[0].getText())
            temp = {}
            temp[item] = td[0].getText()
            dic.update(temp)
        except:
            print("couldn't find")
            pass
        #if count == 2:
        #    break 
    with open("downloads_counts.json", "w") as f:
        json.dump(dic, f)

def main():
    download_counts()

if __name__=="__main__":
    main()
