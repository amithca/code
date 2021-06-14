'''
Consider the problem of finding a path in the grid shown in the following
from the position s to the position g. A piece can move on the grid horizontally or vertically,
 one square at a time. No step may be made into a forbidden shaded area.
1.	On the grid shown in the figure number the nodes expanded (in order) for a DFS, BFS
and IDS from S to g, given that the order of the operators is up, left, right, and down.
 Assume there is cycle pruning. What is the first path found?
2.	For a greedy best-first search from s to g. Manhattan distance should
be used as the evaluation function. The Manhattan distance between two points is
the distance in the x-direction plus the distance in the y-direction. It corresponds to
the distance traveled along city streets arranged in a grid. Assume multiple-path pruning.
 What is the first path found?
3.	For a heuristic depth-first search from s to g, given Manhattan distance as the
evaluation function. Assume cycle pruning. What is the path found?
4.	Number the nodes in order for an A* search, with multiple-path pruning, for the same grid.
 What is the path found?

'''

from collections import deque
from termcolor import colored
ROW = 8
COL = 8


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class queueNode:
    def __init__(self, pt: Point, dist: int):
        self.pt = pt  # The cordinates of the cell
        self.dist = dist  # Cell's distance from the source


def isValid(row: int, col: int):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

''' These arrays are used to get row and column numbers of 4 neighbours of a given cell'''
#order up,left,right,down
rowNum = [-1, 0, 0, 1]
colNum = [0, -1, 1, 0]

''' Function to find the shortest path between a given source cell to a destination cell.'''


def BFS(mat, src: Point, dest: Point):

    '''check source and destination cell of the matrix have value 1'''
    p_cnt=0
    if mat[src.x][src.y] != 1 or mat[dest.x][dest.y] != 1:
        return -1
    visited = [[False for i in range(COL)]
               for j in range(ROW)]
    path_num = [[-1 for i in range(COL)]
               for j in range(ROW)]
    # Mark the source cell as visited
    visited[src.x][src.y] = True
    q = deque()
    # Distance of source cell is 0
    s = queueNode(src, 0)
    q.append(s)  # Enqueue source cell
    # Do a BFS starting from source cell
    while q:
        curr = q.popleft()  # Dequeue the front cell
        pt = curr.pt
        if pt.x == dest.x and pt.y == dest.y:
            print(" BFS Output:")
            display_path(path_num, src, dest)
            return curr.dist
        # Otherwise enqueue its adjacent cells
        for i in range(4):
            row = pt.x + rowNum[i]
            col = pt.y + colNum[i]
            # if adjacent cell is valid, has path and not visited yet, enqueue it.
            if (isValid(row, col) and
                    mat[row][col] == 1 and
                    not visited[row][col]):
                visited[row][col] = True
                p_cnt += 1
                path_num[row][col] = p_cnt
                adjcell = queueNode(Point(row, col), curr.dist + 1)
                q.append(adjcell)
    # Return -1 if destination cannot be reached
    return -1


def DFS(mtx, src: Point, dest: Point):
    # global rowNum
    # global colNum
    # global vis

    # Initialize a stack of pairs and
    # push the starting cell into it
    p_cnt = 0
    st = []
    st.append([src.x, src.y])
    vis = [[False for i in range(COL)] for j in range(ROW)]
    path_num = [[-1 for i in range(COL)]
                for j in range(ROW)]
    # if mtx[src.x][src.y] != 1 or mtx[dest.x][dest.y] != 1:
    #     return -1

    # Iterate until the
    # stack is not empty
    while (len(st) > 0):
        # Pop the top pair
        curr = st[len(st) - 1]
        st.remove(st[len(st) - 1])
        row = curr[0]
        col = curr[1]
        if row == dest.x and col == dest.y:
            print("DFS Output:")
            display_path(path_num, src, dest)
            return -1
        # Check if the current popped
        # cell is a valid cell or not
        if (isValid(row, col) == False):
            continue
        if (vis[row][col]):
            continue;
        if (mtx[row][col] == 0):
            continue
        # Mark the current
        # cell as visited
        vis[row][col] = True

        # Print the element at
        # the current top cell
        # print(mtx[row][col], end=" ")
        p_cnt += 1
        path_num[row][col] = p_cnt

        # Push all the adjacent cells
        for i in range(4):
            adjx = row - rowNum[i]
            adjy = col - colNum[i]
            st.append([adjx, adjy])

def display_board(mtx, src: Point, dst: Point):
    for i in range(ROW):
        for j in range(COL):
            tmp=colored(' ', 'white')
            if mtx[i][j]==0:
                tmp=colored('X', 'white')
            elif i==src.x and j==src.y:
                tmp=colored('S', 'red')
            elif i==dst.x and j==dst.y:
                tmp=colored('G', 'green')
            else:
                tmp=colored(' ', 'white')
            print(f'{tmp}|', end="")
        print("")


def display_path(mtx, src: Point, dst: Point):
    for i in range(ROW):
        for j in range(COL):
            tmp=colored(' ', 'white')
            if i==src.x and j==src.y:
                tmp=colored(' S','red')
            elif i==dst.x and j==dst.y:
                tmp=colored(' G','green')
            elif mtx[i][j] >= 0 and mtx[i][j] <10 :
                tmp = colored(' ', 'white')+colored(mtx[i][j],'white')
            elif mtx[i][j] >= 10:
                tmp = colored(mtx[i][j], 'white')
            else:
                tmp = colored('  ', 'white')

            print(f'{tmp}|', end="")
        print("")
if __name__ == '__main__':
    inp_mat = [[1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 1],
           [1, 1, 0, 1, 1, 1, 0, 1],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1]]
    source = Point(5, 3)
    dest = Point(2, 2)
    print("Input:")
    display_board(inp_mat, source, dest)

    dist = BFS(inp_mat, source, dest)
    if dist != -1:
        print("\nBFS Shortest Path is", dist)
    else:
        print("BFS Shortest Path doesn't exist")
    DFS(inp_mat, source, dest)