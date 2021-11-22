import pulp
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import sys
import os

sources = [2,10,16,22]
nodes = {}
with open(os.path.join(sys.path[0], 'nodes.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        nodes.update( {len(nodes): [float(r) for r in row]} )

edges = {}
with open(os.path.join(sys.path[0], 'edges.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        edges.update( {len(edges): [int(r) for r in row]} )


def calcdistance(i,j):
    return math.sqrt((nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2 + (nodes[i][2]-nodes[j][2])**2)


length = {}
for e in edges:
    length.update( {e: calcdistance(edges[e][0],edges[e][1])} )




# PuLP Model

model = pulp.LpProblem("model", pulp.LpMinimize)

edge_vars = {e:
pulp.LpVariable(cat=pulp.LpInteger, lowBound=0, upBound=1, name="edge_{0}_{1}".format(edges[e][0],edges[e][1])) for e in edges}

for i in nodes:
    if i not in sources:
        model += pulp.lpSum([edge_vars[e] for e in edges if i in edges[e]]) >= 2
    elif i in sources:
        model += pulp.lpSum([edge_vars[e] for e in edges if i in edges[e]]) >= 1

model += pulp.lpSum([edge_vars[e]*length[e] for e in edges])

model.solve()
print("Solution status: ", pulp.LpStatus[model.status])
print("Objective value: ", pulp.value(model.objective))
print([edges[e] for e in edges if pulp.value(edge_vars[e])==1])


# Post-processing

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)
ax.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

for e in edges:
    plt.plot([nodes[edges[e][0]][0], nodes[edges[e][1]][0]], [nodes[edges[e][0]][1], nodes[edges[e][1]][1]], [nodes[edges[e][0]][2],nodes[edges[e][1]][2]], color='gray', marker='.', linestyle='dashed', linewidth=0.5)

for e in edges:
    if pulp.value(edge_vars[e]) == 1:
        i = edges[e][0]
        j = edges[e][1]
        plt.plot([nodes[i][0],nodes[j][0]], [nodes[i][1],nodes[j][1]], [nodes[i][2],nodes[j][2]], color='red', linestyle='dashed', linewidth=1.5)

plt.show()
