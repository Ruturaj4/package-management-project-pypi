import xmlrpc.client as xc
# only one api server so we'll use the deutschland mirror for downloading
client = xc.ServerProxy('https://pypi.python.org/pypi')
packages = client.list_packages()

import os

import tarfile, re, requests, csv, json
from base64 import b64encode
from IPython.utils.path import ensure_dir_exists

def _extract_files(package_file, name, package):
    try:
        tar_file = tarfile.open(fileobj=package_file)
    except:
        return
    temp = []
    for member in tar_file.getmembers():
        if member.isdir():
            #if "/" in member.name:
            if (str(member).count("/")) == 1:
                temp.append((member.name).split("/")[-1])
                #print((member.name).split("/")[-1])
    mydic[package] = temp
                
def extract_package(name, client=xc.ServerProxy('https://pypi.python.org/pypi')):
    try:
        release = client.package_releases(name)[-1]
        outdir = 'pack_info/{}/'.format(name)
        doc = client.release_urls(name, release)
        if doc:
            url = None
            for d in doc:
                if d['python_version'] == 'source' and d['url'].endswith('gz'):
                    url = d['url']
            if url:
                req = requests.get(url)
                if req.status_code != 200:
                    print("Could not download file %s" % req.status_code)
                else:
                    #print(outdir)
                    ensure_dir_exists('{}'.format(outdir))
                    with open('/tmp/temp_tar', 'wb') as tar_file:
                        tar_file.write(req.content)
                    with open('/tmp/temp_tar', 'rb') as tar_file:
                        return _extract_files(tar_file, outdir, name)
    except:
        pass

tot = len(packages)
mydic = {}
ensure_dir_exists('packages')
for i, package in enumerate(packages):
    if i % 100 == 0:
        print('########################Extracting package {} / {}###########################'.format(i+1, tot))
    extract_package(package, client)

with open("packinfo.json", "w") as fp:
    json.dump(mydic, fp)
