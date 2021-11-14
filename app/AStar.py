from PIL import Image, ImageDraw
import numpy as np
import math
from sys import float_info
import heapq as hq

EPS = float_info.epsilon


class Map:

    def __init__(self):
        '''
        Default constructor
        '''

        self.width = 0
        self.height = 0
        self.cells = []

    def ReadFromPNG(self, picture):
        img = Image.open(picture)
        image = np.array(img)
        m = image[::, ::, 1]
        m = m / 255
        m = abs(m - 1)
        self.cells = m.astype(int)

        self.width = image.shape[1]
        self.height = image.shape[0]
        # if you want to get (x,y)  then you should image[y][x]
        # Or if you want to get image[i][j] then you shoud call (j,i)



    def ReadFromString(self, cellStr, width, height):
        """
        Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
        """
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    def SetGridCells(self, width, height, gridCells):
        '''
        Initialization of map by list of cells.
        '''
        self.width = width
        self.height = height
        self.cells = gridCells

    def inBounds(self, i, j):
        '''
        Check if the cell is on a grid.
        '''
        return (0 <= j < self.width) and (0 <= i < self.height)

    def Traversable(self, i, j):
        '''
        Check if the cell is not an obstacle.
        '''
        return not self.cells[i][j]

    def GetNeighbors(self, i, j,):
        neighbors = []
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di != 0 or dj != 0:
                    if self.inBounds(i + di, j + dj) and self.Traversable(i + di, j + dj):
                        neighbors.append([i + di, j + dj])
        return neighbors



class Node:
    """
    Node class represents a search node

    - i, j: coordinates of corresponding grid element
    - g: g-value of the node
    - h: h-value of the node
    - F: f-value of the node
    - parent: pointer to the parent-node

    You might want to add other fields, methods for Node, depending on how you prefer to implement OPEN/CLOSED further on
    """

    def __init__(self, i = 0, j = 0, ID=0, g=0, h=0, F=None, parent=None):
        self.i = i
        self.j = j
        self.ID = ID
        self.g = g
        self.h = h
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent

    def __str__(self):
        return 'Node ' + str(self.j) + ' ' + str(self.i)

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)

    def __lt__(self, other):  # self < other (self has higher priority)
        return self.F < other.F or (abs(self.F - other.F) < EPS and (self.g > other.g))

    def __getID__(self):
        return self.ID


class Open:

    def __init__(self):
        self.elements = []
        self.indexes = {}

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def clear(self):
        self.elements.clear()
        self.indexes.clear()

    def isEmpty(self):
        if len(self.elements) != 0:
            return False
        return True

    def AddNode(self, newNode: Node):

        if self.indexes.get(newNode.ID):
            existingNode = self.indexes[newNode.ID]
            if existingNode.F > newNode.F:
                existingNode.g = newNode.g
                existingNode.F = newNode.F
                existingNode.parent = newNode.parent
                self.indexes[newNode.ID] = existingNode
                hq.heappush(self.elements, newNode)
                return
            else:

                return

        self.indexes[newNode.ID] = newNode
        hq.heappush(self.elements, newNode)

    def GetBestNode(self, *args):

        return hq.heappop(self.elements)


class Closed:

    def __init__(self):
        self.elements = {}

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def clear(self):
        self.elements.clear()

    def AddNode(self, item: Node):
        self.elements[item.ID] = item

    def WasExpanded(self, item: Node):
        return self.elements.get(item.ID)




class Solver:

    def __init__(self, plannerType, map, heuristicFunction):
        self.map = map
        self.plannerType = plannerType
        self.trueGoal = None
        self.heuristicFunction = heuristicFunction
        self.pathFound = False
        self.path = []
        if plannerType == 'astar':
            self.planner = AStar(h=heuristicFunction)

    def __str__(self):
        return 'planner type is: ' + self.plannerType

    def setPlanner(self, plannerType):
        if plannerType == 'astar':
            self.plannerType = plannerType
            self.planner = AStar(h=self.heuristicFunction)
            return True
        else:
            return False

    def plan(self, iStart: int, jStart: int, iGoal: int, jGoal: int):
        self.planner.clear()
        result = self.planner.plan(self.map, iStart, jStart, iGoal, jGoal)
        if result[0]:
            self.trueGoal = result[1]
        else:
            self.trueGoal = Node()
        return result[0]

    def MakePath(self):
        """
        Creates a path by tracing parent pointers from the goal node to the start node
        It also returns path's length.
        """

        length = self.trueGoal.g
        current = self.trueGoal
        self.path = []
        while current.parent:
            self.path.append(current)
            current = current.parent
        self.path.append(current)
        return self.path[::-1], length

    def MakePathRaw(self):
        """
        Creates a path by tracing parent pointers from the goal node to the start node
        It also returns path's length.
        """

        length = self.trueGoal.g
        current = self.trueGoal
        path = []
        while current.parent:
            path.append([current.j, current.i])
            current = current.parent
        path.append([current.j, current.i])
        return path[::-1], length


class Planner:

    def __init__(self):
        self.Open = Open()
        self.Closed = Closed()

    def clear(self):
        self.Open.clear()
        self.Closed.clear()

    def plan(self, gridMap: Map, iStart: int, jStart: int, iGoal: int, jGoal: int):
        return False, Node(iGoal, jGoal, ID=iGoal * gridMap.width + jGoal)


class AStar(Planner):

    def __init__(self, h):
        self.Open = Open()
        self.Closed = Closed()
        self.h = h

    def ComputeCost(self, i1, j1, i2, j2):
        """
        Computes cost of simple moves between cells
        """
        if abs(i1 - i2) + abs(j1 - j2) == 1:  # cardinal move
            return 1
        else:  # diagonal move
            return math.sqrt(2)

    def plan(self, gridMap: Map, iStart: int, jStart: int, iGoal: int, jGoal: int):
        start = Node(iStart, jStart, ID=iStart * gridMap.width + jStart)
        start.h = self.h(iStart, jStart, iGoal, jGoal)
        start.F = start.h
        self.Open.AddNode(start)
        print('Start: ' + str(jStart) + ' ' + str(iStart))
        print('Goal: ' + str(jGoal) + ' ' + str(iGoal))
        while not self.Open.isEmpty():
            curNode = self.Open.GetBestNode()
            # print('Open size:', len(self.Open))
            # print('Closed size:', len(self.Closed))
            # print('Current Node: ' + str(curNode.j) + ' ' + str(curNode.i))
            if curNode.i == iGoal and curNode.j == jGoal:
                return True, curNode

            neighbors = gridMap.GetNeighbors(curNode.i, curNode.j)
            for node in neighbors:
                newNode = Node(node[0], node[1])
                if not self.Closed.WasExpanded(newNode):
                    newNode.g = curNode.g + self.ComputeCost(curNode.i, curNode.j, newNode.i, newNode.j)
                    newNode.h = self.h(newNode.i, newNode.j, iGoal, jGoal)
                    newNode.F = newNode.g + newNode.h
                    newNode.parent = curNode
                    newNode.ID = newNode.i * gridMap.width + newNode.j
                    self.Open.AddNode(newNode)

            self.Closed.AddNode(curNode)

        return False, Node()

