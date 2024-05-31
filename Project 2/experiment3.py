import random

'''This program will generate a 8x8 map with random heights from range 1 - 5. 
An agent starting at a random location will take 10 steps try and find the maximum height. 
If the agent has has not found the max height, then agent will restart and another location
and take another 10 steps

@authors: Phuoc Le
          Phuc Le
          Matthew Maksim
@date: 10/5/2022 
'''

def main():
    '''this function will start the program'''
    # blank map
    Map = [[0, 0, 0, 0, 0, 0, 0, 0], 
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0]]
    
    for i in range(8):  # fill the map with 1-5 then print it
        for j in range(8):
            num = getheight()
            Map[i][j] = num
        print(Map[i])

    max = 0
    for i in range(8):  # find the highest height in the map
        for j in range(8):
            if max < Map[i][j]:
                max = Map[i][j]
            
    print("\nhighest number:", max)
    
    startx = random.randint(0, 7)  # generate a x and y coordinate for starting position
    starty = random.randint(0, 7)
    global position
    position = (startx, starty)
    print("\nstarting at: (", startx, ",", starty, ")\ncurrent height:", Map[position[0]][position[1]])

    for i in range(10):  # the agent move 10 steps
        move(Map)
        print("\ncurrent position:", position, "\ncurrent height:", Map[position[0]][position[1]])
    # if agent cant find global max, restart at another location and step 10 more steps
    if Map[position[0]][position[1]] < max:
        print("\nrestart")
        startx = random.randint(0, 7)
        starty = random.randint(0, 7)
        position = (startx, starty)
        for i in range(10):
            move(Map)
            print("\ncurrent position:", position, "\ncurrent height:", Map[position[0]][position[1]])
    

def move(Map):  # move function that choose the first highest neighbor to move to
    '''this function will make the agent to take a step'''
    global position
    temp = (position[0], position[1])
    for x in range(position[0] - 1, position[0] + 2):
        for y in range(position[1] - 1, position[1] + 2):
            if x >= 0 and x < len(Map):
                if y >= 0 and y < len(Map[x]):
                    if Map[x][y] >= Map[temp[0]][temp[1]]:
                        if abs(Map[x][y] - Map[position[0]][position[1]]) <= 1:
                            temp = (x, y)
    position = temp
    return 0
    

def getheight(): # function that return a number from 1-5
    '''this function will generate a random height from 1-5'''
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
