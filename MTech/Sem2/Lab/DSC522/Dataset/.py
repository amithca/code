
import time
import random
from statistics import mean
import networkx as nx
import matplotlib.pyplot as plt


class BfsDfsComplexityAnalysis():

    def __init__(self, file, test_node_count):
        self.G = nx.Graph()
        self.file = file
        self.test_node_count = test_node_count

    def analyse(self):

        self.G, nodes = self.load_data(self.file, self.G)

        nodes = self.get_sample_nodes(nodes, self.test_node_count)

        # paths = nx.shortest_path_length(G, "1001", "1025")
        # paths = nx.shortest_path(G, "1001", "1025")
        # print(paths)
        dfs_elapsed_times = self.get_dfs_time_complexity(self.G, nodes)
        bfs_elapsed_times = self.get_bfs_time_complexity(self.G, nodes)
        self.plot_time_complexity(x_coordinates=nodes,  y1_coordinates=dfs_elapsed_times,
                                  y2_coordinates=bfs_elapsed_times)
        self.plot_time_complexity_with_average(x_coordinates=nodes,  y1_coordinates=dfs_elapsed_times,
                                               y2_coordinates=bfs_elapsed_times)
        # nx.draw(bfs, with_labels=True, font_weight='bold')
        # plt.show()

    def load_data(self, file, G):
        file = open(file, 'r')
        # nodes = ["1001", "9401139", "9505162", "9506126", "9610201",
        #         "9507118", "107017", "9806154", "203228", "211259"]
        node_list = []
        for line in file:
            if not line.startswith("#"):
                (vertex1, sep, vertex2) = line.partition("\t")
                vertex1 = vertex1.strip()
                vertex2 = vertex2.strip()
                node_list.append(vertex1)
                G.add_node(vertex1)
                G.add_edge(vertex1, vertex2)
            else:
                print(line)

        file.close()
        list_set = set(node_list)
        nodes = (list(list_set))

        return G, nodes

    def get_sample_nodes(self, nodes, no_of_nodes):
        indexes = random.sample(range(1, len(nodes)), no_of_nodes)
        sample_nodes = []
        for index in indexes:
            sample_nodes.append(nodes[index])
        return sample_nodes

    def get_dfs_time_complexity(self, G, nodes):
        elapsed_times = []
        for node in nodes:
            start = time.time()
            dfs = nx.dfs_tree(G, node)
            end = time.time()
            dfs_time = end - start
            elapsed_times.append(dfs_time)
        return elapsed_times

    def get_bfs_time_complexity(self, G, nodes):
        elapsed_times = []
        for node in nodes:
            start = time.time()
            bfs = nx.bfs_tree(G, node)
            end = time.time()
            bfs_time = end - start
            elapsed_times.append(bfs_time)
        return elapsed_times

    def plot_time_complexity(self, x_coordinates, y1_coordinates, y2_coordinates):

        plt.xlabel("Node")
        plt.ylabel("Time Complexity")
        plt.xticks(rotation=45)
        plt.plot(x_coordinates, y1_coordinates, '-rD', label='DFS')
        plt.plot(x_coordinates, y2_coordinates, '-bD', label='BFS')
        plt.legend()
        # plt.show()
        plt.savefig('dfs_bfs_time_complexity.png')
        plt.close()

    def plot_time_complexity_with_average(self, x_coordinates, y1_coordinates, y2_coordinates):

        plt.xlabel("Node")
        plt.ylabel("Time Complexity")
        plt.xticks(rotation=45)
        y1_mean = [mean(y1_coordinates)]*len(x_coordinates)
        y2_mean = [mean(y2_coordinates)]*len(x_coordinates)
        plt.plot(x_coordinates, y1_coordinates, '-rD', label='DFS')
        plt.plot(x_coordinates, y2_coordinates, '-bD', label='BFS')
        plt.plot(x_coordinates, y1_mean, '-r', label='Mean', linestyle='--')
        plt.plot(x_coordinates, y2_mean, '-b', label='Mean', linestyle='--')
        plt.legend()
        plt.show()
        # plt.savefig('dfs_bfs_avg_time_complexity.png')
        # plt.close()


complexity_analysis = BfsDfsComplexityAnalysis(
    file="Cit-HepTh.txt", test_node_count=25)
complexity_analysis.analyse()
