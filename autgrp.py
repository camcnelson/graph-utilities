import pynauty as nty

import networkx as nx
import pygraphviz as pgv

import csv
import os, sys



E = {}
n = 0

with open(os.path.join(sys.path[0], 'edges.csv'), newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		v_from = int(row[0])
		v_to = int(row[1])
		if(v_from in E):
			E[v_from].append(v_to)
		else:
			E.update({v_from : [v_to]})
		n = max(n, v_from+1, v_to+1)

G = nty.Graph(n, directed = False)
for e in E:
	G.connect_vertex(e, E[e])

print(nty.autgrp(G))


# nxG = nx.Graph()
# for e in E:
# 	for i in E[e]:
# 		nxG.add_edge(e,i)


# # visualization
# AG = nx.nx_agraph.to_agraph(nxG)
# AG.node_attr["shape"] = "circle"
# AG.node_attr["style"] = "filled"
# AG.node_attr["fillcolor"] = "white"
# AG.node_attr["fontcolor"] = "black"
# AG.layout()
# AG.draw(os.path.join(sys.path[0], "graphSym.png"))
