import random, math
'''This program will generate a 8x8 map with random heights from range 1 - 5. 
An agent starting at a random location will take 20 steps using the hill climbing
algorithm to try and find the maximum height

@authors: Phuoc Le
          Phuc Le
          Matthew Maksim
@date: 10/5/2022 
'''
    
def SIMULATED_ANNEALING(current, schedule):
    '''this function will make the agent move using the simulated annealing algorithm'''
    global Map, max
    for t in range(9999): # t will increase each cycle
        T = schedule - t # as t get bigger, T gets smaller
        if T == 0: # if T is 0, return
            return current
        neighbor = [] # list of neighbor

        for x in range(current[0] - 1, current[0] + 2): # finall al neighbor from current position
            for y in range(current[1] - 1, current[1] + 2):
                if x >= 0 and x < len(Map): # make sure x in in range
                    if y >= 0 and y < len(Map[x]): # make sure y is in range
                        if x != current[0] and y != current[1]: # check if not current position
                            neighbor.append((x, y))
        
        if len(neighbor) < 1: # if there are no more neighbor then return
            return current
        
        next = neighbor[random.randint(0, len(neighbor)) - 1] # choose a random neighbor
        
        delta = Map[next[0]][next[1]] - Map[current[0]][current[1]] # check the hegight difference of current and next
        if delta > 0: # If next is higher than current, go
            current = next
            print("\ncurrent position:", current, "\ncurrent height:", Map[current[0]][current[1]])
            if Map[current[0]][current[1]] == max: # if current height is max return
                print("\nmax reached")
                return current
        else:
            chance = math.e**(delta / T) # chance to make current = next
            if random.random() <= chance:
                current = next
                print("\ncurrent position:", current, "\ncurrent height:", Map[current[0]][current[1]])

def getheight(): # function that return a number from 1-5
    '''this function will generate a height number from 1-5'''
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

def main():
    '''this function will start the program'''
    # blank map
    global Map
    Map = [[0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]
    
    for i in range(8): # fill the map with 1-5 then print it
        for j in range(8):
            num = getheight()
            Map[i][j] = num
        print(Map[i])
    global max
    max = 0
    for i in range(8): # find the highest height in the map
        for j in range(8):
            if max < Map[i][j]:
                max = Map[i][j]
    print("\nMax height:", max)
    startx = random.randint(0, 7) # generate a x and y coordinate for starting position
    starty = random.randint(0, 7)
    global position # starting position
    position = (startx, starty)
    print("\nstarting at: (", startx, ",", starty, ")\ncurrent height:", Map[position[0]][position[1]])
    
    SIMULATED_ANNEALING(position, 20)
    
main()
