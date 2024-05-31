import sys
import math
import heapq

'''This program will take 2 arguments from the command line: a text file 
containing an explorer map, and a heuristic function code.

@authors: Phuoc Le
          Phuc Le
          Matthew Maksim
@date: 9/16/2022 
'''

# Dictionary with char value as key compare to height
heightValues = {
        "~": 0,
        ".": 1,
        ":": 2,
        "M": 3,
        "S": 4
    }
# Dictionary with int value as key compare to character
charValues = {
        0: "~",
        1: ".",
        2: ":",
        3: "M",
        4: "S"
    }


class Node:
    '''A node class to represent a map with'''
    
    def __init__(self, state, pathCost, hCost):
        '''Initializes Node object with a state, pathCost, and hCost.
        Also contains a list of child nodes and a parent.
        '''
        self.state = state
        self.pathCost = pathCost
        self.hCost = hCost
        self.child = []
        self.parent = None
    
    def goalTest(state):
        '''This function accepts a state map as input and returns
        true if the explorer on the map.
        '''
        for i in state:
            if "4" in i:
                return True
        return False

    def action(state):
        '''This function accepts a state map as input and will return a list of 
        coordinates around the explorer(3x3), in which all height differences of > 1 will be removed.
        '''
        explorerPosition = [0, 0, 0]
        for i in range(len(state)): # loop to find the explorer position in the state map
            for j in range(len(state[i])):
                h = state[i][j]
                if h == "0" or h == "1" or h == "2" or h == "3" or h == "4":
                    explorerPosition[0] = i
                    explorerPosition[1] = j
                    explorerPosition[2] = h

        #find all neighbor (exclude out of bound and height difference > 1)
        neighborList = []
        eX = explorerPosition[0]
        eY = explorerPosition[1]
        eZ = explorerPosition[2]
        for x in range(eX-1, eX+2):
            for y in range(eY-1, eY+2):
                if x >= 0 and x < len(state):  # exclude if out of bound x
                    if y >= 0 and y < len(state[x]):  # exclude if out of bound y
                        if x != eX or y != eY: # exclude if current position
                            neighborList.append((x, y))

        for coords in neighborList.copy():# loop to remove height differences > 1
            if abs(heightValues[state[coords[0]][coords[1]]] - int(eZ)) >= 2: 
                neighborList.remove(coords)

        return neighborList

    def updateState(state, action):
        '''This function accept a state map and an action as input. 
        An action is the coordinate that the explorer will want to move to.
        The function will then move the explorer to the action coordinate and return the new state map.
        '''
        explorerPosition = [0, 0, 0]
        
        copyState = []
        for row in state: # copy the state map
            tempC = []
            for c in row:
                tempC.append(c)
            copyState.append(tempC)
            
        for i in range(len(copyState)): # loop to find the explorer position
            for j in range(len(copyState[i])):
                h = copyState[i][j]
                if h == "0" or h == "1" or h == "2" or h == "3" or h == "4":
                    explorerPosition[0] = i
                    explorerPosition[1] = j
                    explorerPosition[2] = h
                    
        eX = explorerPosition[0] # explorer x coordinate
        eY = explorerPosition[1] # explorer y coordinate
        copyState[action[0]][action[1]] = str(heightValues[copyState[action[0]][action[1]]]) # use dictionary to swap map character to height value
        copyState[eX][eY] = charValues[int(copyState[eX][eY])] # use dictionary to swap explorer height value to map character
        return copyState

    def heuristicCost(state):
        '''This function accepts a state map and find the distance between the explorer and the summit.
        '''
        summitPosition = [0, 0, 0]
        explorerPosition = [0, 0, 0]
        for i in range(len(state)): # loop to find summit and explorer position
            for j in range(len(state[i])):
                h = state[i][j]
                if h == "0" or h == "1" or h == "2" or h == "3" or h == "4":
                    explorerPosition[0] = i
                    explorerPosition[1] = j
                    explorerPosition[2] = h
                if state[i][j] == "S":
                    summitPosition[0] = i
                    summitPosition[1] = j
                    summitPosition[2] = 4
        
        if sys.argv[2] == "0": # normal 3D euclidean distance
            return math.sqrt(
                (explorerPosition[0] - summitPosition[0]) ** 2
                + (explorerPosition[1] - summitPosition[1]) ** 2
                + (int(explorerPosition[2]) - summitPosition[2]) ** 2
            )
        elif sys.argv[2] == "1": # the 3D manhattan distance
            return abs((explorerPosition[0] - summitPosition[0]) 
                + (explorerPosition[1] - summitPosition[1])
                + (int(explorerPosition[2]) - summitPosition[2])
            )
        elif sys.argv[2] == "2": # the 2D (x and y only) euclidean distance
            return math.sqrt(
                (explorerPosition[0] - summitPosition[0]) ** 2
                + (explorerPosition[1] - summitPosition[1]) ** 2
            )
        else: # if invalid heuristic formula code, exit
            print("error: invalid heuristic argument")
            exit(1)

def a_star_search(problem):
    '''This function takes a problem state map that contain an explorer and a summit. 
    The function will use the A-star algorithm to find a path for the explorer to reach the summit.
    '''

    # create a root node with 0 path cost and a heuristic cost to goal 
    node = Node(problem, 0, Node.heuristicCost(problem))
    
    frontier = [(0, 0, node)] # a list of nodes to explore
    heapq.heapify(frontier)
    explored = [] # a list of nodes that have been explored
    counter = 1  # counter to break ties in frontier

    while True: # while loop to find the path from initial position to the summit
        
        if len(frontier) == 0: # if frontier is empty, exit
            print("Fail to find path")
            exit(1)
        tup = heapq.heappop(frontier) # get next node that contain the next state map
        node = tup[2]
        if Node.goalTest(node.state): # if state map of node pass goalTest, then return the node
            return node
        explored.append(node) # if not at goal, then add node to already explored list

        
        # for all direction that the explorer can move to
        for action in Node.action(node.state):
            newState = Node.updateState(node.state, action) # create a new state for this action

            # find path and heuristic cost
            heuristicCost = Node.heuristicCost(newState)
            pathCost = node.pathCost + heuristicCost
            childNode = Node(newState, pathCost, heuristicCost)

            # set relationship between child and parent node
            node.child.append(childNode)
            childNode.parent = node

            addFrontier = True
            tempfCost = 0
            if childNode not in explored: # if childNode is not already explored
                for testNode in frontier.copy(): # Loop to find childNode is in frontier
                    if testNode[2].state == childNode.state:
                        addFrontier = False
                        tempfCost = testNode[0]
                if addFrontier:
                    counter = counter + 1
                    heapq.heappush(frontier, (pathCost, counter, childNode)) # if childNode is not in explored list and frontier add it to frontier
            elif not addFrontier or pathCost < tempfCost: # if childNode is in frontier list but with a smaller cost
                for testNode in frontier.copy():
                    if testNode[2].state == childNode.state:
                        counter = counter + 1
                        frontier.remove(testNode)
                        heapq.heappush(frontier, (childNode.pathCost, counter, childNode)) # add childNode in frontier
            counter = counter + 1 # increment the counter

def main():
    '''Main function will run first'''
    
    if len(sys.argv) != 3:
        print("Invalid missing or no arguments")
        sys.exit(1)

    summitPosition = [0, 0, 0]

    try:
        # reads in lines of text file
        with open(sys.argv[1], "r") as file:
            data = file.readlines()
        # stores each line as an element of an array and remove any \n character
        for i in range(len(data)):
            data[i] = data[i].replace("\n", "")
    except FileNotFoundError:
        print("File Not Found")
        sys.exit(1)

    # get a 2d array of the terrain
    problem = [list(line) for line in data]

    # print the first initial state map (Map 0)
    print("\nM_0")
    for i in range(len(problem)):
        temp = ""
        for j in range(len(problem[i])):
            temp = temp + problem[i][j]
        print(temp)
    print("\n")
    
    for i in range(len(problem)): # loop to find the summit position
        for j in range(len(problem[i])):
            if problem[i][j] == "S":
                summitPosition[0] = i
                summitPosition[1] = j
                summitPosition[2] = 4

    solution = a_star_search(problem) # get the solution node
    
    draw(solution) # draw the path leading to the goal state

def draw(node):
    '''this function will take the solution node and 
    trace it back to the root node and  print the map of each node'''
    
    allNode = [] # a list containing all node to solution
    allNode.append(node) # all root node into list
    while node.parent is not None: # trace solutuon node to root
        allNode.append(node.parent)
        node = node.parent

    mapNum = "1"
    allNode.remove(allNode[len(allNode) - 1]) # remove the duplicate begining node
    
    for i in reversed(allNode): # for each node in list print its map
        print("M_" + str(mapNum))
        for a in range(len(i.state)):
            ad = ""
            for j in range(len(i.state[a])):
                ad = ad + i.state[a][j]
            print(ad)
        mapNum = int(mapNum) + 1
        print("\n")

main() # run the main function
