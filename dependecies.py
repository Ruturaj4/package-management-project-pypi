import pandas as pd
from collections import defaultdict
import os
import requirements
import numpy as np
import xmlrpc.client as xc

client = xc.ServerProxy('https://pypi.python.org/pypi')
packages = client.list_packages()

datadict = defaultdict(list)
with open('requirements.txt', 'r') as infile:
    new_package = True
    for line in infile:
        if line.strip() == '':
            new_package = True
            print(package_name)
            if package_name not in datadict['package']:
                datadict['package'].append(package_name)
                datadict['requirement'].append(np.nan)
            continue

        if new_package:
            # If this is the case, the current line gives the name of the package
            package_name = os.path.basename(line).strip()
            new_package = False
        else:
            # This line gives a requirement for the current package
            try:
                print(line)
                for req in requirements.parse(line.strip()):
                    datadict['package'].append(package_name)
                    datadict['requirement'].append(req.name)
            except ValueError:
                pass


# Convert to dataframe
df = pd.DataFrame(data=datadict)
df.head()

df['package_name'] = np.nan
df['package_version'] = np.nan
for i, package in enumerate(packages):
    try:
        if i % 100 == 0:
            print('Package {}: {}'.format(i+1, package))
        for release in client.package_releases(package):
            try:
                pkg_str = '{}-{}'.format(package, release)
                idx = df.loc[df.package == pkg_str].index
                if len(idx) > 0:
                    df.loc[idx, 'package_name'] = package
                    df.loc[idx, 'package_version'] = release
            except:
                pass
    except:
        pass
df.head()

df.to_csv('requirements.csv', index=False)
