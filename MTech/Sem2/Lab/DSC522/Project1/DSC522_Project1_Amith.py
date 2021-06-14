'''
Amith C A
2020MCS120003
DSC522 Lab Assignment 1
'''
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
from statistics import mean
from fpdf import FPDF

pwd = 'C:/Users/amith/OneDrive/MTech/Sem2/Lab/DSC522/'
start_node = 0
goal_node = 380
output_file_name = 'DSC522_Project1_BFS_DFS_Analysis'
dfs = []
bfs=''
class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        # w = self.get_string_width(title) + 6
        # self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        #self.cell(w, 9, title, 1, 1, 'C', 1)
        # Line break
        self.ln(10)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.2)
        self.rect(5, 5, 200, 287, 'D');

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 16)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, ' %s' % ( label), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        # Read text file
        with open(f'{pwd}content/txt/{name}', 'r') as f:
            txt = f.read()

        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')
        #self.cell(0, 5, '(end of excerpt)')

    def print_chapter(self, num, title, name):
        # self.add_page()
        self.chapter_title(num, title)
        self.ln(15)
        self.chapter_body(name)


def dfs_paths(g, start, goal, path=None):
    time.sleep(0.001)
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next in set(g[start]) - set(path):
        yield from dfs_paths(g, next, goal, path + [next])


def BFS_SP(g, start, goal):
    explored = []
    path = []
    queue = [[start]]
    if start == goal:
        print("Same Node")
        return
    while queue:
        time.sleep(0.001)
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = g[node]
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    # print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)
    print("Connecting" \
          "path doesn't exist :(")
    return


def get_dfs_time_complexity(graph, start_node, sample_nodes):
    elapsed_times = []
    for node in sample_nodes:
        if node != start_node:
            dfs_time = get_dfs_time(graph, start_node, node)
            elapsed_times.append(dfs_time)
    return elapsed_times


def get_bfs_time_complexity(graph, start_node, sample_nodes):
    elapsed_times = []
    for node in sample_nodes:
        if node != start_node:
            bfs_time = get_bfs_time(graph, start_node, node)
            elapsed_times.append(bfs_time)
    return elapsed_times


def get_dfs_time(T, start, goal):
    dfs = []
    start_time = time.time()
    dfs = list(dfs_paths(T, start, goal))
    end_time = time.time()
    print(f'Start={start}, Goal={goal}, DFS Shortest path = {dfs[0]}')
    elapsed_time = end_time - start_time
    return elapsed_time


def get_bfs_time(T, start, goal):
    start_time = time.time()
    bfs = BFS_SP(T, start, goal)
    end_time = time.time()
    print(f'Start={start}, Goal={goal}, BFS Shortest path = {bfs}')
    elapsed_time = end_time - start_time
    return elapsed_time


def set_colour(graph, shortest_path):
    node_colors = []
    for n in graph.nodes():
        if n == start_node:
            node_colors.append("yellow")
        elif n == goal_node:
            node_colors.append("green")
        elif n in shortest_path:
            node_colors.append("cyan")
        else:
            node_colors.append("red")
    return node_colors


def create_graph_img(g, g_colors, file_name):
    nx.draw(g, with_labels=True, font_weight='bold', node_color=g_colors)
    plt.savefig(f'{pwd}/tmp/{file_name}.png')
    plt.clf()


def create_graph(graph, file):
    for line in file:
        if not line.startswith("#"):
            (vertex1, sep, vertex2) = line.partition("\t")
            vertex1 = vertex1.strip()
            vertex2 = vertex2.strip()
            graph.add_edge(int(vertex1), int(vertex2))
    return graph


def plot_time_complexity(x_coordinates, y1_coordinates, y2_coordinates, file_name):
    plt.xlabel("Node")
    plt.ylabel("Time (s))")
    plt.xticks(rotation=45)
    plt.plot(x_coordinates, y1_coordinates, '-rD', label='DFS')
    plt.plot(x_coordinates, y2_coordinates, '-bD', label='BFS')
    plt.legend()
    plt.savefig(f'{pwd}/tmp/{file_name}.png')
    plt.clf()


def plot_time_complexity_with_average(x_coordinates, y1_coordinates, y2_coordinates, file_name):
    plt.xlabel("Node")
    plt.ylabel("Time (s))")
    plt.xticks(rotation=45)
    y1_mean = [mean(y1_coordinates)] * len(x_coordinates)
    y2_mean = [mean(y2_coordinates)] * len(x_coordinates)
    plt.plot(x_coordinates, y1_coordinates, '-rD', label='DFS')
    plt.plot(x_coordinates, y2_coordinates, '-bD', label='BFS')
    plt.plot(x_coordinates, y1_mean, '-r', label='Mean', linestyle='--')
    plt.plot(x_coordinates, y2_mean, '-b', label='Mean', linestyle='--')
    plt.legend()
    # plt.show()
    plt.savefig(f'{pwd}/tmp/{file_name}.png')
    plt.clf()

def generate_report(pwd, output_file_name):
    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297
    pdf = PDF('P', 'mm', 'A4')  # Page format
    page_title = 'Bfs Dfs ComplexityAnalysis'
    pdf.set_author('Amith C A')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 30)
    '''Page : 1'''
    w = pdf.get_string_width(page_title) + 15
    pdf.set_draw_color(0, 80, 180)
    pdf.set_fill_color(255, 255, 255) #white
    pdf.set_text_color(0, 0, 0) #black
    pdf.ln(PAGE_HEIGHT * .3)
    pdf.cell(w, 15, page_title, 1, 1, 'C', 1)

    pdf.ln(PAGE_HEIGHT * .3)
    pdf.set_font('Arial', '', 10)
    pdf.cell(w, 15, 'Amith C A', 0, 1, 'R', 1)
    pdf.cell(w, 15, '2020MCS120003', 0, 1, 'R', 1)
    pdf.cell(w, 15, 'DSC523 Project 1', 0, 1, 'R', 1)

    '''Page : 2'''
    pdf.add_page()
    pdf.print_chapter(1, 'Computational Complexity', 'Computational_complexity_intro.txt')
    pdf.ln(20)
    pdf.print_chapter(1.1, 'Time Complexity', 'Time_complexity_into.txt')

    '''Page : 3'''
    pdf.add_page()
    pdf.print_chapter(2, 'Big-O Notation', 'Big_O_intro.txt')
    node_list = []
    pdf.set_font('Arial', 'BU', 10)
    pdf.write(10, "Table of common time complexities")
    pdf.ln(15)
    pdf.set_font('Arial', '', 10)
    big_o_table = {
        "Constant Time": "O(1)",
        "Logarithmic Time": "O(log n)",
        "Linear Time": "O(n)",
        "Quasilinear Time": "O(n log n)",
        "Quadratic Time": "O(n^2)",
        "Exponential Time": "O(2^n)",
        "Factorial Time": "O(n!)"
    }
    pdf.cell(40, 7, 'Name', 1)
    pdf.cell(40, 7, 'Time Complexity', 1)
    pdf.ln()
    for key, value in big_o_table.items():
        pdf.cell(40, 6, key, 1)
        pdf.cell(40, 6, value, 1)
        pdf.ln()
    '''Page : 4'''
    pdf.add_page()
    pdf.print_chapter(3, 'Input Graph', 'Input_graph_desc.txt')
    pdf.write(10, "Input graph plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/input_graph.png', 15, 80, PAGE_WIDTH - 40)
    '''Page  : 5'''
    pdf.add_page()
    pdf.print_chapter(3, 'Depth First Search', 'DFS.txt')
    '''Page : 6'''
    pdf.add_page()
    pdf.chapter_title(3, 'DFS Tree')
    pdf.set_font('Arial', '', 10)
    pdf.write(10, f'The Shortest path from start node {start_node} to goal node {goal_node} is : {dfs[0]}')
    pdf.ln(20)
    pdf.write(10, "DFS Tree plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/dfs_tree_shortest_path.png', 15, 60, PAGE_WIDTH - 40)
    '''Page : 7'''
    pdf.add_page()
    pdf.print_chapter(4, 'Breadth First Search', 'BFS.txt')
    pdf.ln(20)
    pdf.add_page()
    # pdf.set_font('Arial', 'B', 16)
    pdf.chapter_title(4.1, 'BFS Tree')
    pdf.set_font('Arial', '', 10)
    pdf.write(10, f'The Shortest path from start node {start_node} to goal node {goal_node} is : {bfs}')
    pdf.ln(20)
    pdf.write(10, "BFS Tree plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/bfs_tree_shortest_path.png', 15, 60, PAGE_WIDTH - 40)
    '''Page : 8'''
    pdf.add_page()
    pdf.chapter_title(3, 'BFS vs DFS')
    pdf.ln(15)
    bfs_vs_dfs = {"BFS": "DFS",
"BFS stands for Breadth First Search.": "DFS stands for Depth First Search.",
"BFS(Breadth First Search) uses Queue data structure for finding the shortest path.": "DFS(Depth First Search) uses Stack data structure.",
"BFS can be used to find single source shortest path in an unweighted graph, because in BFS, we reach a vertex with minimum number of edges from a source vertex.": "In DFS, we might traverse through more edges to reach a destination vertex from a source.",
"BFS is more suitable for searching vertices which are closer to the given source.": "DFS is more suitable when there are solutions away from source.",
"BFS considers all neighbors first and therefore not suitable for decision making trees used in games or puzzles.": "DFS is more suitable for game or puzzle problems. We make a decision, then explore all paths through this decision. And if this decision leads to win situation, we stop.",
"The Time complexity of BFS is O(V + E) when Adjacency List is used and O(V^2) when Adjacency Matrix is used, where V stands for vertices and E stands for edges.": "The Time complexity of DFS is also O(V + E) when Adjacency List is used and O(V^2) when Adjacency Matrix is used, where V stands for vertices and E stands for edges."}
    pdf.ln(0.1)
    pdf.set_font('Arial', '', 8)
    for key, value in bfs_vs_dfs.items():
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(70, 10, key, 1)
        y2 = pdf.get_y()
        pdf.set_xy(x + 70, y)
        pdf.multi_cell(70, 10, value, 1)
        x = pdf.get_x()
        pdf.set_xy(x, y2)
        # pdf.ln()
    '''Page : 9'''
    pdf.add_page()
    # pdf.set_font('Arial', 'BU', 16)
    pdf.chapter_title(5, 'Time complexity analysis of BFS vs DFS')
    # pdf.write(10, "Time complexity analysis of BFS vs DFS")
    pdf.ln(20)
    pdf.set_font('Arial', '', 10)
    pdf.write(10, f'The time complexity plot of BFS vs DFS is as below:')
    pdf.image(f'{pwd}tmp/time_complexity.png', 15, 60, PAGE_WIDTH - 40)
    '''Page : 10'''
    pdf.add_page()
    # pdf.set_font('Arial', 'BU', 16)
    pdf.chapter_title(6, 'Time complexity analysis of BFS vs DFS (Average)')
    # pdf.write(10, "Time complexity analysis of BFS vs DFS (Average)")
    pdf.ln(20)
    pdf.set_font('Arial', '', 10)
    pdf.write(10, f'The time complexity plot of BFS vs DFS is as below:')
    pdf.image(f'{pwd}tmp/time_complexity_avg.png', 15, 60, PAGE_WIDTH - 40)
    '''Page : 11'''
    pdf.add_page()
    pdf.print_chapter(3, 'Conclusion', 'Inference.txt')
    pdf.output(f'{pwd}/{output_file_name}.pdf', 'F')

if __name__ == '__main__':
    graph = nx.Graph()

    with open(f'{pwd}/Dataset/roadNet-CA_Copy.txt', 'r') as f:
        graph = create_graph(graph, f)
    graph_colors = []
    for n in graph.nodes():
        graph_colors.append("orange")
    create_graph_img(graph, graph_colors, 'input_graph')
    dfs_tree = nx.dfs_tree(graph, source=start_node, depth_limit=None)
    bfs_tree = nx.bfs_tree(graph, source=start_node, depth_limit=None)


    dfs = list(dfs_paths(dfs_tree, start_node, goal_node))
    print('DFS Shortest path = ', dfs[0])
    bfs = BFS_SP(bfs_tree, start_node, goal_node)
    print('BFS Shortest path = ', bfs)
    '''Create Shortest path image'''
    dfs_node_colors = set_colour(dfs_tree, dfs[0])
    create_graph_img(dfs_tree, dfs_node_colors, 'dfs_tree_shortest_path')
    bfs_node_colors = set_colour(bfs_tree, bfs)
    create_graph_img(bfs_tree, bfs_node_colors, 'bfs_tree_shortest_path')
    '''Calculate time complexities'''
    no_of_nodes = 25
    nodes = graph.nodes()
    print('nodes=', set(nodes))
    # sample_nodes = random.sample(set(nodes) - set([start_node]), no_of_nodes)
    sample_nodes = [1, 15, 26, 34, 77, 84, 95, 109, 119, 123]

    print('sample_nodes=', sample_nodes)
    dfs_elapsed_times = get_dfs_time_complexity(dfs_tree, start_node, sample_nodes)
    bfs_elapsed_times = get_bfs_time_complexity(bfs_tree, start_node, sample_nodes)
    # print(dfs_elapsed_times)
    plot_time_complexity(x_coordinates=sample_nodes, y1_coordinates=dfs_elapsed_times,
                         y2_coordinates=bfs_elapsed_times, file_name='time_complexity')
    plot_time_complexity_with_average(x_coordinates=sample_nodes, y1_coordinates=dfs_elapsed_times,
                                      y2_coordinates=bfs_elapsed_times, file_name='time_complexity_avg')
    generate_report(pwd, output_file_name)
