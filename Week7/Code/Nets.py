#!/usr/bin/env python3
"""visualise qmee ctd collab net"""

__author__ = 'Yuchen YANG (YY5819@ic.ac.uk)'
__version__ = '0.0.1'

import networkx as nx
import scipy as sc
import matplotlib.pyplot as p
import matplotlib.patches as patches
import pandas as pd
import ipdb

# Open csv
links = pd.read_csv("../Data/QMEE_Net_Mat_edges.csv", header=0)
nodes = pd.read_csv("../Data/QMEE_Net_Mat_nodes.csv", header=0)


count = links.shape[0]
# ipdb.set_trace()
# set column name to match row id to create cordinates system
links.columns = list(range(count))

# init list for of links, wrights, and colors 
linklist = []
weights = []
color = []

for i in range(count):
    for j in range(count):
        if links[i][j] > 0:
            #[(id, id, weight)]
            linklist.append((i,j))
            #width for edges, with very basic scaling
            weights.append(links[i][j])

for i in nodes.Type:
    if i == 'University':
        color.append('b')
    elif i == 'Hosting Partner':
        color.append('g')
    else:
        color.append('r')
        
# normalise weight list       
normed_weights = [1 + i/10 for i in weights]



# add layout basiced on item index
G = nx.DiGraph()

pos = nx.spring_layout(nodes.index.values) 
# add data to graph object
G.add_nodes_from(nodes.index.values)
G.add_edges_from(linklist)

# initialise plot
p.axis('off')
# draw the graph
nx.draw_networkx(G, pos, 
    node_color = color, 
    node_size = 2000, 
    with_labels = False, 
    width = normed_weights,
    edge_color = 'grey')
# nx.draw_networkx_edges(G, pos, width = normed_weights, edge_color = 'grey')
# add lable from nodes
nx.draw_networkx_labels(G, pos, nodes["id"])

# create legends
blue = patches.Patch(color='b', label='University')
green = patches.Patch(color='g', label='Hosting Partner')
red = patches.Patch(color='r', label='Non-Hosting Partner')
p.legend(handles=[blue, green, red])
p.savefig('../Results/Nets_py.svg')
p.close()
