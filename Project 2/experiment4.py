import random

'''This program will generate a 8x8 map with random heights from range 1 - 5. 
An agent starting at a random location will take 20 steps using the hill climing beam
algorithm to try and find the maximum height

@authors: Phuoc Le
          Phuc Le
          Matthew Maksim
@date: 10/5/2022 
'''

visited = [] # all visited coordinates
frontier = [] # current best nodes

def main():
    '''this function will start the program'''
    global visited, frontier
    Map = [[0, 0, 0, 0, 0, 0, 0, 0], 
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]]
   
    # create map
    for i in range(8): 
        for j in range(8):
            num = getheight()
            Map[i][j] = num
        print(Map[i])
        
    # get highest height on the map
    max = 0 
    for i in range(8):
        for j in range(8):
            if max < Map[i][j]:
                max = Map[i][j]
    # get a list of coordinates of max height on map
    maxList = []
    for i in range(8):
        for j in range(8):
            if max == Map[i][j]:
                maxList.append((i, j))
    
    print("\nhighest number:", max)
    
    startx = random.randint(0, 7)
    starty = random.randint(0, 7)
    position = (startx, starty)
    visited.append(position)

    # get the closest max height from starting position
    global closestMax
    closestMax = maxList[0]
    for x in maxList:
        if getDistance(position, closestMax) > getDistance(position, x):
            closestMax = x
    print("starting at: (", startx, ",", starty, ")\ncurrent height:", Map[position[0]][position[1]], "\nclosest max height:", closestMax)

    getStartingFrontier(Map, position)
    print("\nstarting frontier:", frontier, "\n")
    
    # move to find maximum
    for i in range(20):
        move(Map)
        print("frontier:", frontier)
        for i in frontier:
            if Map[i[0]][i[1]] == max:
                print("\nMax reached")
                return


def getStartingFrontier(Map, position):
    '''this function will generate the starting frontier from the starting position
    '''
    global visited, frontier, closestMax
    
    bestList = []
    for x in range(position[0] - 1, position[0] + 2):
        for y in range(position[1] - 1, position[1] + 2):
            if x >= 0 and x < len(Map): # make sure x in in range
                if y >= 0 and y < len(Map[x]): # make sure y is in range
                    if Map[x][y] >= Map[position[0]][position[1]]: # make sure neighbor is >= itself
                        if abs(Map[x][y] - Map[position[0]][position[1]]) <= 1: # make sure delta of neighbor and current is 1
                            bestList.append((x, y))
    
    if len(bestList) >= 2:
        best = bestList[0]
        for x in bestList:
            if getDistance(best, closestMax) > getDistance(x, closestMax):
                best = x
        bestList.remove(best)
        frontier.append(best)
        visited.append(best)
    if len(bestList) >= 1:
        secondBest = bestList[0]
        for x in bestList:
            if getDistance(secondBest, closestMax) > getDistance(x, closestMax):
                secondBest = x
        frontier.append(secondBest)
        visited.append(secondBest)

def getDistance(start, end):
    '''this function will return the distance between the closest max height and the current position
    '''
    return ((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5

def move(Map):
    '''this function will make the agent move for each frontier'''
    global visited, frontier, closestMax
    bestList = []
    for i in range(len(frontier)): # for each coordinates in frontier
        position = frontier[i]
        for x in range(position[0] - 1, position[0] + 2):
            for y in range(position[1] - 1, position[1] + 2):
                if x >= 0 and x < len(Map): # make sure x in in range
                    if y >= 0 and y < len(Map[x]): # make sure y is in range
                        if Map[x][y] >= Map[position[0]][position[1]]: # make sure neighbor is >= itself
                            if abs(Map[x][y] - Map[position[0]][position[1]]) <= 1: # make sure delta of neighbor and current is 1
                                if not (x, y) in visited: # make sure neighbor has never been visited
                                    bestList.append((x, y))

    frontier.clear()
    
    if len(bestList) >= 2:
        best = bestList[0]
        for x in bestList:
            if getDistance(best, closestMax) > getDistance(x, closestMax):
                best = x
        bestList.remove(best)
        frontier.append(best)
    if len(bestList) >= 1:
        secondBest = bestList[0]
        for x in bestList:
            if getDistance(secondBest, closestMax) > getDistance(x, closestMax):
                secondBest = x
        frontier.append(secondBest)
    return 0
    

def getheight():
    '''this function will generate a height from 1-5
    '''
    done = False
    while not done:
        if random.randint(0, 1) == 1:
            return 1
        if random.randint(0, 1) == 1:
            return 2
        if random.randint(0, 1) == 1:
            return 3
        if random.randint(0, 1) == 1:
            return 4
        if random.randint(0, 1) == 1:
            return 5

main()
