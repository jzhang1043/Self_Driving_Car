from collections import deque
import numpy as np
from queue import PriorityQueue
import lab1_part2_map as mp
import heapq

class Node():
    def __init__(self, parent = None, pos = None):
        self.parent = parent
        self.pos = pos
        self.f = 0
        self.g = 0
        self.h = 0
        # initialize for A star calculation
    
# return the calculated manhattan heuristic
def manhattan_dist(currPos, dest):
    return abs(currPos[0] - dest[0]) + abs(currPos[1] - dest[1])

# return the calculated path we have found
def traceBack(parent, dest):
    robPath = [dest]
    while(robPath[-1] in parent):
        # append the parent
        robPath.append(parent(robPath[-1]))
    robPath.reverse()
    return robPath

# get the accurate 30 x 30 car size
def carPosition(coord):
    x, y = coord[0], coord[1]
    return [(x, y-15), (x, y+15) (x+30, y-15), (x+30, y+15)]


def getAvNodesAround(currNode):
    x, y = currNode[0], currNode[1]
    carPos = [(x, y-15), (x, y+15) (x+30, y-15), (x+30, y+15)]
    nodesAround = []
    #forward
    nodesAround.append((x - 1, y))
    #backward
    nodesAround.append((x + 1, y))
    #lefthand
    nodesAround.append((x, y - 1))
    #righthand
    nodesAround.append((x, y + 1))
    
    return nodesAround
    pass

def getShortestPath(begin, end, map):
    all_parents = {}
    # queue used for a* search 
    q = []
    #track points visited
    visited = []
     # set all g, h, f to zero 
    begin.g = 0
    begin.h = 0
    begin.f = 0 
    #beginNode = Node(None, (begin[0], begin[1]))
    
    end.g = 0
    end.h = 0
    end.f = 0 
    #endNode = Node(None, (end[0], end[1]))
    q.append((0,begin))
    visited.append(begin)
    
    #dictionary for all g values
    all_g = {}
    all_g[begin] = 0
    
    while(q):
        temp_node = heapq.heappop(q)
        curr_node = temp_node[1]
        
        if (curr_node == end) :
            # Reached the final node
            break
        # get all ava neighbor nodes
        nodesAround = getAvNodesAround(curr_node)
        for avaNode in nodesAround:
            if avaNode not in all_g:
                all_g[avaNode] = all_g[curr_node] + 1
                # get heristic distance of each neighbor node
                fx = manhattan_dist(avaNode, end) + (all_g[avaNode])
                # push fx val and the near nodes to que
                heapq.heappush(q, (fx, avaNode))
                # set neighbor parent to current node
                all_parents[avaNode] = curr_node
    
    return traceBack(all_parents, end)      
        
    pass