import xmlrpc.client as xc
# only one api server so we'll use the deutschland mirror for downloading
client = xc.ServerProxy('https://pypi.python.org/pypi')
packages = client.list_packages()

import os

import tarfile, re, requests, csv, json
from base64 import b64encode
from IPython.utils.path import ensure_dir_exists

def _save_file(pathname, member, tar_file):
    try:
        content = tar_file.extractfile(member).read()
    except:
        return
    print(pathname)
    print(os.path.basename(member.name))
    outfilename = os.path.basename(member.name)
    #outfilename = '{}{}'.format(pathname, os.path.basename(member.name))
    #ensure_dir_exists(outfilename)
    with open(os.path.join(pathname, outfilename), 'wb') as outfile:
        outfile.write(content)
    return

def _extract_files(package_file, name):
    try:
        tar_file = tarfile.open(fileobj=package_file)
    except:
        return
    for member in tar_file.getmembers():
        if 'setup.py' in member.name or 'requirements' in member.name:
            _save_file(name, member, tar_file)
                
def extract_package(name, client=xc.ServerProxy('https://pypi.python.org/pypi')):
    for release in client.package_releases(name):
        try:
            outdir = 'packages/{}-{}/'.format(name, release)
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
                            return _extract_files(tar_file, name=outdir)
        except:
            pass

ensure_dir_exists('packages')
for i, package in enumerate(packages):
    if i % 100 == 0:
        print('Extracting package {} / {}'.format(i+1, len(packages)))
    #print(package)

    extract_package(package, client)
