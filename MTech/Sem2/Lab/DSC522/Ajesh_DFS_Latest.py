import networkx as nx
import matplotlib.pyplot as plt

def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in set(graph[start]) - set(path):
        yield from dfs_paths(graph, next, goal, path + [next])

def set_colour(graph,shortest_path):
    node_colors = []
    for n in graph.nodes():
        if n == start_node:
            node_colors.append("yellow")
        elif n == goal_node:
            node_colors.append("green")
        elif n in shortest_path:
            node_colors.append("blue")
        else:
            node_colors.append("red")
    return node_colors


if __name__ == '__main__':
    graph = nx.Graph()
    pwd = 'C:/Users/amith/OneDrive/MTech/Sem2/Lab/DSC522/'
    file = open(f'{pwd}/Dataset/roadNet-CA.txt', 'r')
    for line in file:
        if not line.startswith("#"):
            (vertex1, sep, vertex2) = line.partition("\t")
            vertex1 = vertex1.strip()
            vertex2 = vertex2.strip()
            graph.add_edge(int(vertex1), int(vertex2))

        else:
            print(line)

    print(graph.edges)

    print(list(nx.dfs_preorder_nodes(graph, source=0)))
    start_node = 0
    goal_node = 380
    print(nx.shortest_path(graph,start_node,goal_node))
    dfs=[]
    dfs=list(dfs_paths(graph, start_node, goal_node))
    print(dfs[0])
    dfs_tree=nx.dfs_tree(graph, source=start_node, depth_limit=None)
    # node_colors = ["blue" if n in dfs[0] else "red" for n in graph.nodes()]
    node_colors=set_colour(dfs_tree, dfs[0])
    # nx.draw(graph, with_labels=True, font_weight='bold',node_color=node_colors)
    nx.draw(dfs_tree, with_labels=True, font_weight='bold', node_color=node_colors)

    plt.show()
