import puzzle
from Queue import Queue
from Queue import LifoQueue
from Queue import PriorityQueue
import node
import sys

class Search:

    def __init__(self, puzzle):
        self.start = node.Node(puzzle)

    def iterativeDeepening(self):
        depth = 0
        result = None
        while result == None:
            result = self.depthLimited(depth)
            depth +=1
        return result
    
