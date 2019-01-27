import os, re
import json

def author():
    os.chdir("packages")
    print(os.getcwd())
    main_dic = []
    for f in os.listdir():
        os.chdir(f)
        print(os.listdir())
        try:
            with open("setup.py", "r") as f:
                temp = f.readlines()
        except:
            os.chdir("../")
            continue
        dic = {}
        for line in temp:
            t = []
            if 'name=' in line:
                ln = "".join(line.split())
                ln = re.search("name='(.+?)',", ln)
                if ln:
                    ln = ln.group(1)
                    ln = ln.strip('\"')
                    ln = ln.strip("\'")
                    dic[ln] = []
            if 'author=' in line:
                la = "".join(line.split())
                la = re.search("author='(.+?)',", la)
                if la:
                    la = la.group(1)
                    la = la.strip('\"')
                    la = la.strip("\'")
                    t.append(la)
                    dic[ln] = t
            if 'author_email=' in line:
                le = "".join(line.split())
                le = re.search("author_email='(.+?)',", le)
                if le:
                    le = le.group(1)
                    le = le.strip('\"')
                    le = le.strip("\'")
                    t.append(le)
                    dic[ln] = t
                    break
        try:
            print(dic)
            main_dic.update(dic)
        except:
            pass
        os.chdir("../")
    #print(main_dic)
    with open('author-pypi.json', 'w') as fp:
        json.dump(main_dic, fp)

def main():
    author()

if __name__=="__main__":
    main()
