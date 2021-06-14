from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


def BFS_SP(graph, start, goal):
    explored = []
    path =[]
    queue = [[start]]
    if start == goal:
        print("Same Node")
        return
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)
    print("Connecting" \
          "path doesn't exist :(")
    return


if __name__ == "__main__":
    graph = nx.Graph()
    file = open('roadNet-CA.txt', 'r')
    for line in file:
        if not line.startswith("#"):
            (vertex1, sep, vertex2) = line.partition("\t")
            vertex1 = vertex1.strip()
            vertex2 = vertex2.strip()
            graph.add_edge(int(vertex1), int(vertex2))

        else:
            print(line)

    print(graph.edges)
    path=[]
    path=BFS_SP(graph, 0, 380)
    print('typeee>>>>',type(path))


    print(type(nx.shortest_path(graph,0, 380)))
    #path=nx.shortest_path(graph,0, 98)
    print('>>>>>>>>',path)
    node_colors = ["blue" if n in path else "red" for n in graph.nodes()]
    nx.draw_networkx(graph, with_labels=True, node_color=node_colors)
    plt.show()

