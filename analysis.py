from __future__ import print_function, division

import pandas as pd
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt
from matplotlib import patches

import seaborn as sns
import operator
import numpy as np
sns.set_context('notebook', font_scale=1.5)
sns.set_style('white')

requirements = pd.read_csv('requirements.csv')

def make_graph(df, min_edges=0):
    DG = nx.DiGraph()
    DG.add_nodes_from(df.package_name.unique())
    edges = df.loc[df.requirement.notnull(), ['package_name', 'requirement']].values
    DG.add_edges_from(edges)

    # Remove bad nodes
    DG.remove_nodes_from(['.', 'nan', np.nan])

    deg = DG.degree()
    #print(deg)
    try:
        to_remove = [n for n in deg if deg[n] <= min_edges]
        DG.remove_nodes_from(to_remove)
    except:
        #print("key not present")
        pass
    return DG

#DG = make_graph(requirements, min_edges=10)
#write_dot(DG, 'requirements_graph.dot')

#dep_graph = make_graph(requirements, min_edges=0)

#print(len(dep_graph.node))
G = make_graph(requirements)
print(G.number_of_edges())

def dependency_graph():
    deplist = []

    for node in G:
        if len(G[node]) == 0:
            continue
        deplist.append(len(G.out_edges([node])))
    x = zero_to_nan(deplist)
    x = np.sort(x)
    print(x)
    print(len(x))
    p = 1. * np.arange(len(x))/(len(x) - 1)
    plt.plot(x, p, marker='.', linestyle='none')
    _ = plt.xlabel('Dependencies')
    _ = plt.ylabel('CDF')
    plt.margins(0.02)
    plt.show()

def zero_to_nan(values):
    return [float('nan') if x==0 else x for x in values ]

def pageRank():
    #Calculate the page rank
    pr = {}
    pr = nx.pagerank(G)
    pr = sorted(pr.values(), reverse=True)
    return pr

max_d = []

def dfs_depth(G, source=None, depth_limit=None):
    if source is None:
        nodes = G
    else:
        nodes = [source]
    visited = set()
    if depth_limit is None:
        depth_limit = len(G)
    for start in nodes:
        print(start)
        if start in visited:
            continue
        max_depth = 0
        visited.add(start)
        stack = [(start, depth_limit, iter(G[start]))]
        while stack:
            parent, depth_now, children = stack[-1]
            try:
                child = next(children)
                if child not in visited:
                    yield parent, child
                    visited.add(child)
                    if depth_now > 1:
                        if((depth_limit - depth_now + 1)>max_depth):
                            max_depth = depth_limit - depth_now + 1
                        stack.append((child, depth_now - 1, iter(G[child])))
            except StopIteration:
                stack.pop()
    global max_d
    max_d.append(max_depth)

def deplist(pr):
    # Calculate all the dependencies, dependents
    dcon = {}
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    for node in G:
        print(node)
        #temp = {node:len(G.out_edges(node))}
        list1.append(node)
        list2.append(len(G.out_edges(node)))
        list3.append(len(G.in_edges(node)))
        list4.append(len(list(nx.dfs_edges(G,node))))
        list(dfs_depth(G, node))
        #dcon.update(temp)
    list2 = sorted(list2, reverse=True)
    list3 = sorted(list3, reverse=True)
    list4 = sorted(list4, reverse=True)
    global max_d
    max_d = sorted(max_d, reverse=True)
    df = pd.DataFrame(data={"Dependencies":list2[:1000], "Dependents":list3[:1000], "DFS-Edges":list4[:1000], "Max-Depth":max_d[:1000], "Page Rank":pr[:1000]})
    df.plot(kind="density", subplots=True, layout=(3,2), sharex=False)
    plt.show()

#pr = pageRank()
#deplist(pr)

#dependency_graph()

print(G.in_edges())

#sorted_dict = sorted(G.in_degree().items(), key=operator.itemgetter(1))[::-1]

N = 10
x = np.arange(N)
y = np.array([d[1] for d in sorted_dict[:N]])
xlabels = [d[0] for d in sorted_dict[:N]][::-1]
fig, ax = plt.subplots(1, 1, figsize=(7, 7))

ax.barh(x[::-1], y, height=1.0)
ax.set_yticks(x + 0.5)
_ = ax.set_yticklabels(xlabels)
ax.set_xlabel('Number of Connections')
ax.set_title('Graph Degree')
fig.subplots_adjust(left=0.27, bottom=0.1, top=0.95)
fig.show()

