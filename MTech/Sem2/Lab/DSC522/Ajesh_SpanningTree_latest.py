import networkx as nx
import matplotlib.pyplot as plt

def set_colour(graph,start_node):
    node_colors = []
    for n in graph.nodes():
        if n == start_node:
            node_colors.append("Red")
        else:
            node_colors.append("cyan")
    return node_colors

G = nx.Graph()

file = open('roadNet-CA.txt', 'r')
for line in file:
    if not line.startswith("#"):
        (vertex1, sep, vertex2) = line.partition("\t")
        vertex1 = vertex1.strip()
        vertex2 = vertex2.strip()
        G.add_edge(int(vertex1), int(vertex2))

    else:
        print(line)
#mst=nx.prim_mst(G)# a generator of MST edges

BFStree = nx.bfs_tree(G,2)
DFStree = nx.dfs_tree(G,2)
minTree=nx.minimum_spanning_tree(G,2)

nx.draw(BFStree,with_labels=True,node_color=set_colour(BFStree,2))
plt.show()

nx.draw(DFStree,with_labels=True,node_color=set_colour(BFStree,2))
plt.show()

nx.draw(minTree,with_labels=True,node_color=set_colour(BFStree,2))
plt.show()