import pandas as pd
from collections import defaultdict
import numpy as np

df = pd.read_csv("requirements.csv")

class Tree(object):
    def __init__(self, name):
        self.name = name
        self.children = []
        return

    def __contains__(self, obj):
        return obj == self.name or any([obj in c for c in self.children])
    
    def add(self, obj):
        if not self.__contains__(obj):
            self.children.append(Tree(obj))
            return True
        return False
    
    def get_base_requirements(self):
        base = []
        for child in self.children:
            if len(child.children) == 0:
                base.append(child.name)
            else:
                for b in [c.get_base_requirements() for c in child.children()]:
                    base.extend(b)
        return np.unique(base)
    

def get_requirements(package):
    return df.loc[(df.package_name == package) & (df.requirement.notnull()), 'requirement'].values


def get_dependency_tree(package, tree):
    reqs = get_requirements(package)
    for req in reqs:
        #print(req)
        flg = tree.add(req)
        if not flg:
            continue
        tree = get_dependency_tree(req, tree)
    return tree

datadict = defaultdict(list)
for i, package in enumerate(df.package_name.unique()):
    if i % 100 == 0:
        print('Package {}: {}'.format(i+1, package))
    try:
        deptree = get_dependency_tree(package, Tree(package))
    except:
        print('Failure getting base dependencies for {}'.format(package))
        raise ValueError
    for dependency in deptree.get_base_requirements():
        datadict['package_name'].append(package)
        datadict['requirements'].append(dependency)

base_df = pd.DataFrame(data=datadict)
base_df.head()

base_df.to_csv('base_requirements.csv', index=False)
