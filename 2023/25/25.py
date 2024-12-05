# import matplotlib.pyplot as plt
import networkx as nx

with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")

connections = {line.split(": ")[0]: line.split(": ")[1].split(" ") for line in data}

g = nx.Graph()

for node, conn in connections.items():
    for other in conn:
        g.add_edge(node, other)

# plt.figure(figsize=(20, 20))
# nx.draw(g, node_size=5, with_labels=True, font_size=12, edge_color=[0.8, 0.8, 0.8])

edges_to_remove = [{"xvp", "zpc"}, {"vfs", "dhl"}, {"pbq", "nzn"}]
g0 = nx.Graph()
for node, conn in connections.items():
    for other in conn:
        if {node, other} in edges_to_remove:
            # print(f"Skip adding {node} --> {other}")
            continue
        g0.add_edge(node, other)

answer_1 = 1
for cc in nx.connected_components(g0):
    answer_1 *= len(cc)
print(answer_1)
