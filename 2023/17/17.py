from collections import deque

import networkx as nx
import numpy as np

INFINITY = float("inf")


with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")

# +
M = np.array([[int(x) for x in line] for line in data])
G = nx.DiGraph(nx.grid_graph(dim=M.shape))
nrows, ncols = M.shape

# Add weights
for row in range(nrows):
    for col in range(ncols):
        vi = (col, row)
        wi = M[row, col]
        if col < ncols - 1:
            vj = (col + 1, row)
            wj = M[row, col + 1]
            G.edges[(vi, vj)]["weight"] = wj
            G.edges[(vj, vi)]["weight"] = wi
        if row < nrows - 1:
            vk = (col, row + 1)
            wk = M[row + 1, col]
            G.edges[(vi, vk)]["weight"] = wk
            G.edges[(vk, vi)]["weight"] = wi
# -

A = dict(G.adjacency())

for node, props in A[(0, 0)].items():
    print(node, props["weight"])

source = (0, 0)
target = (12, 12)

path = nx.shortest_path(G, source, target)
d = 0
for i in range(len(path) - 1):
    # d += M[row, col]
    v0 = path[i]
    v1 = path[i + 1]
    d += A[v0][v1]["weight"]
print(d)

nx.shortest_path_length(G, source, target)

# +

"""Uses Dijkstra's algorithm to determine the shortest path from
source to target. Returns (path, distance).
"""

unvisited_nodes = list(G.nodes)  # All nodes are initially unvisited.

# Create a dictionary of each node's distance from source. We will
# update each node's distance whenever we find a shorter path.
distance_from_start = {node: (0 if node == source else INFINITY) for node in G.nodes}

# Initialize previous_node, the dictionary that maps each node to the
# node it was visited from when the the shortest path to it was found.
previous_node = {node: None for node in G.nodes}

while unvisited_nodes:
    # Set current_node to the unvisited node with shortest distance
    # calculated so far.
    current_node = min(unvisited_nodes, key=lambda node: distance_from_start[node])
    unvisited_nodes.remove(current_node)

    # If current_node's distance is INFINITY, the remaining unvisited
    # nodes are not connected to source, so we're done.
    if distance_from_start[current_node] == INFINITY:
        break

    # For each neighbor of current_node, check whether the total distance
    # to the neighbor via current_node is shorter than the distance we
    # currently have for that node. If it is, update the neighbor's values
    # for distance_from_start and previous_node.
    # for neighbor, distance in self.adjacency_list[current_node]:
    for neighbor, properties in A[current_node].items():
        distance = properties["weight"]
        new_path = distance_from_start[current_node] + distance
        if new_path < distance_from_start[neighbor]:
            distance_from_start[neighbor] = new_path
            previous_node[neighbor] = current_node

    if current_node == target:
        break  # we've visited the destination node, so we're done

# To build the path to be returned, we iterate through the nodes from
# target back to source. Note the use of a deque, which can
# appendleft with O(1) performance.
path = deque()
current_node = target
while previous_node[current_node] is not None:
    path.appendleft(current_node)
    current_node = previous_node[current_node]
path.appendleft(source)

d = distance_from_start[target]
print(d)
