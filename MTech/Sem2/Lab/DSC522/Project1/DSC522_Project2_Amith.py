'''
Amith C A
2020MCS120003
DSC522 Lab Assignment 2
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
output_file_name = 'DSC522_Project2_SpanningTree'
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



def set_colour(graph, start_node):
    node_colors = []
    for n in graph.nodes():
        if n == start_node:
            node_colors.append("red")
        else:
            node_colors.append("cyan")
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

def generate_report(pwd, output_file_name):
    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297
    pdf = PDF('P', 'mm', 'A4')  # Page format
    page_title = 'Spanning Tree'
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

    pdf.ln(PAGE_HEIGHT * .35)
    pdf.set_font('Arial', '', 10)
    pdf.ln(.3)
    pdf.cell(w+70, 15, 'Amith C A', 0, 1, 'R', 1)
    pdf.cell(w+70, 15, '2020MCS120003', 0, 1, 'R', 1)
    pdf.cell(w+70, 15, 'DSC522 Project 2', 0, 1, 'R', 1)

    '''Page : 2'''
    pdf.add_page()
    pdf.print_chapter(1, 'Minimum Spanning tree', 'Minimum_spanning_tree.txt')
    pdf.ln(20)


    '''Page : 3'''
    pdf.add_page()
    pdf.print_chapter(3, 'Input Graph', 'Input_graph_desc.txt')
    pdf.write(10, "Input graph plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/input_graph_spanning.png', 15, 80, PAGE_WIDTH - 40)
    '''Page  : 5'''
    pdf.add_page()
    pdf.print_chapter(3, 'Depth First Search', 'DFS.txt')
    '''Page : 6'''
    pdf.add_page()
    pdf.chapter_title(3, 'DFS Tree')
    pdf.set_font('Arial', '', 10)
    # # pdf.write(10, f'The Shortest path from start node {start_node} to goal node {goal_node} is : {dfs[0]}')
    # # pdf.ln(20)
    # pdf.write(10, "DFS Tree plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/dfs_tree_spanning.png', 15, 60, PAGE_WIDTH - 40)
    '''Page : 7'''
    pdf.add_page()
    pdf.print_chapter(4, 'Breadth First Search', 'BFS.txt')
    pdf.ln(20)
    pdf.add_page()
    # pdf.set_font('Arial', 'B', 16)
    pdf.chapter_title(4.1, 'BFS Tree')
    # pdf.set_font('Arial', '', 10)
    # pdf.write(10, f'The Shortest path from start node {start_node} to goal node {goal_node} is : {bfs}')
    # pdf.ln(20)
    # pdf.write(10, "BFS Tree plot: ")
    # pdf.ln(20)
    pdf.image(f'{pwd}tmp/bfs_tree_spanning.png', 15, 60, PAGE_WIDTH - 40)

    '''Page : 8'''
    pdf.add_page()
    pdf.chapter_title(3, 'Minimum spanning Tree')
    pdf.set_font('Arial', '', 10)
    # # pdf.write(10, f'The Shortest path from start node {start_node} to goal node {goal_node} is : {dfs[0]}')
    # # pdf.ln(20)
    # pdf.write(10, "DFS Tree plot: ")
    pdf.ln(20)
    pdf.image(f'{pwd}tmp/minimum_spanning.png', 15, 60, PAGE_WIDTH - 40)

    '''Page : 11'''
    pdf.add_page()
    pdf.print_chapter(3, 'Conclusion', 'Conclusion_spanning_tree.txt')
    pdf.output(f'{pwd}/{output_file_name}.pdf', 'F')

if __name__ == '__main__':
    graph = nx.Graph()

    with open(f'{pwd}/Dataset/roadNet-CA_Copy.txt', 'r') as f:
        graph = create_graph(graph, f)
    graph_colors = []
    for n in graph.nodes():
        graph_colors.append("orange")
    create_graph_img(graph, graph_colors, 'input_graph_spanning')
    dfs_tree = nx.dfs_tree(graph, source=start_node, depth_limit=None)
    bfs_tree = nx.bfs_tree(graph, source=start_node, depth_limit=None)

    dfs = list(dfs_paths(dfs_tree, start_node, goal_node))
    print('DFS Shortest path = ', dfs[0])
    bfs = BFS_SP(bfs_tree, start_node, goal_node)
    print('BFS Shortest path = ', bfs)
    '''Create Shortest path image'''
    dfs_node_colors = set_colour(dfs_tree, start_node)
    create_graph_img(dfs_tree, dfs_node_colors, 'dfs_tree_spanning')
    bfs_node_colors = set_colour(bfs_tree, start_node)
    create_graph_img(bfs_tree, bfs_node_colors, 'bfs_tree_spanning')

    plt.clf()
    minTree = nx.minimum_spanning_tree(graph, 2)
    minTree_node_colors = set_colour(minTree, start_node)
    # nx.draw(minTree, with_labels=True, node_color=minTree_node_colors)
    # plt.show()
    create_graph_img(minTree, minTree_node_colors, 'minimum_spanning')
    generate_report(pwd, output_file_name)
    # plt.clf()