import pulp
import random
import time
import math
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import sys
import os

# nodes are 3-tuples of coordinates
# nodes are supplied as a csv, where the ith row is the three coordinates of the ith node
nodes = {}
with open(os.path.join(sys.path[0], 'nodes.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        nodes.update( {len(nodes): tuple(float(r) for r in row)} )
sources = set([2,10,16,22])

# edges are 2-tuples of node indices
# edges are supplied as a csv, where the ith row is the two indices of the nodes that edge i connects.
# edges are directed
edges = {}
with open(os.path.join(sys.path[0], 'edges.csv'), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        edges.update( {len(edges): tuple(int(r) for r in row)} )

def calcDistance(i,j):
    return math.sqrt((nodes[i][0]-nodes[j][0])**2
        + (nodes[i][1]-nodes[j][1])**2
        + (nodes[i][2]-nodes[j][2])**2)

# get adjacency matrix:
intAdj = np.zeros((len(nodes),len(nodes)), dtype=int)
lengthAdj = np.zeros((len(nodes),len(nodes)), dtype=float)
for i in range(len(nodes)):
    for j in range(len(nodes)):
        if (i,j) in edges.values():
            intAdj[i,j] = 1
            lengthAdj[i,j] = calcDistance(i,j)

# need valid path to start
oddNodes = []
for n in nodes:
    if sum([1 for i in nodes if intAdj[n,i]>0]) % 2 == 1:
        oddNodes.append(n)

def Dijkstra(i,j,wadj):
    unreached = list(range(wadj.shape[0]))
    reachable = []
    reached = [i]
    unreached.remove(i)
    dist = np.full(wadj.shape[0], 10000000, dtype=float)
    dist[i] = 0
    prev = np.zeros(wadj.shape[0], dtype=int)
    while True:
        if j in reached:
            prevlist = []
            k = j
            while k!=i:
                prevlist.insert(0,k)
                k = prev[k]
            prevlist.insert(0,i)
            return (dist[j],[(prevlist[i],prevlist[i+1]) for i in range(len(prevlist)-1)])
        for m in reached:
            for n in unreached:
                if wadj[m,n] > 0:
                    if dist[m] + wadj[m,n] < dist[n]:
                        dist[n] = dist[m] + wadj[m,n]
                        prev[n] = m
                    reachable.append(n)
        if len(reachable) == 0:
            return None
        reached.clear()
        reached = reachable.copy()
        reachable.clear()
    return None

oddAdj = np.zeros((len(oddNodes),len(oddNodes)))
for i in range(len(oddNodes)):
    for j in range(len(oddNodes)):
        oddAdj[i,j] = Dijkstra(oddNodes[i],oddNodes[j],lengthAdj)[0]


# PuLP min T-join model
model = pulp.LpProblem("minimum T-join", pulp.LpMinimize)

# variables:
useEdge = {(i,j): pulp.LpVariable(cat=pulp.LpBinary, lowBound=0, name="create_edge_{0}_{1}".format(i,j)) for i in range(len(oddNodes)) for j in range(len(oddNodes))}

# constraints:
for i in range(len(oddNodes)):
    for j in range(len(oddNodes)):
        model += useEdge[(i,j)] == useEdge[(j,i)]
for i in range(len(oddNodes)):
    model += pulp.lpSum([useEdge[(i,j)] for j in range(len(oddNodes)) if j!=i]) == 1

# objective:
model += pulp.lpSum([oddAdj[i,j]*useEdge[i,j] for i in range(len(oddNodes)) for j in range(len(oddNodes))])

model.solve()

FleuryAdj = intAdj.copy()
for i in range(len(oddNodes)):
    for j in range(len(oddNodes)):
        if pulp.value(useEdge[(i,j)])==1:
            for (m,n) in Dijkstra(oddNodes[i],oddNodes[j],lengthAdj)[1]:
                FleuryAdj[m,n] += 1
                # print("Including edge: ", oddNodes[i],oddNodes[j])

#DFScount
def DFS(i,adj,visited):
    visited[i] = 1
    for j in nodes:
        if adj[i,j] == 1 and visited[j] == 0:
            DFS(j,adj,visited)

def DFScount(i,adj):
    visited = [0 for j in range(adj.shape[0])]
    DFS(i,adj,visited)
    return sum(visited)

# Fleury's Algorithm
path = []
i = 0
path.append(i)
j = 0
while True:
    if j >= len(nodes):
        break
    if FleuryAdj[i,j] > 0:
        ctWith = DFScount(i,FleuryAdj)
        FleuryAdj[i,j] = FleuryAdj[j,i] = FleuryAdj[j,i]-1
        ctWithout = DFScount(i,FleuryAdj)
        if sum(FleuryAdj[i,:])==0: # if j is the only node connected to i
            # print(i,"--bridge-->", j)
            path.append(j)
            i = j
            j = 0
            continue
        elif ctWith==ctWithout: # if i,j is not a bridge
            # print(i,"-->", j)
            path.append(j)
            i = j
            j = 0
            continue
        else:
            FleuryAdj[i,j] = FleuryAdj[j,i] = FleuryAdj[j,i]+1
            j += 1
            continue
    else:
        j += 1

print("Postman's path: ", path)
# print(int(len(edges)/2))
# print(len(path)-1)
