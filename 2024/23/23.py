import networkx as nx

G = nx.Graph()
G.add_edges_from([e.split("-") for e in open("input.txt").read().split("\n")])

# Part 1: count cycles with length 3 where at least one node starts with "t"
ans1 = len(list(filter(lambda c: any(x[0] == "t" for x in c), nx.simple_cycles(G, 3))))

# Part 2: find largest complete subgraph
ans2 = ",".join(sorted(max(nx.find_cliques(G), key=len)))

print(ans1)
print(ans2)
