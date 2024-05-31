'''This program will let the user play connect 4 flip game with a bot.
the bot will be using the minimax algorithm with alpha-beta pruning to 
find the best moves against the player.

@authors: Phuoc Le
          Phuc Le
          Matthew Maksim
@date: 10/7/2022 
'''

possibleLetters = ["a", "b", "c", "d", "e","f", "g", "h"]  # the possible row for board
possibleNums = ["1", "2", "3", "4", "5"]                   # the possible column for the board
possibleFlip = ["1", "2", "3", "4", "5", "n"]              # the possible flip arguments
rows = 8  # number of rows the board have
cols = 5  # number of column the board have


def main():
    '''this function will start the game of connect 4 Spin'''
    
    # the game board
    gameBoard = [["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"]]

    print("\nWelcome to Connect Four Spin Game")
    print("---------------------------------")
    print("\nWhich player would you like to play (R/Y)?")
    global humanChip
    humanChip = input()                          # color of the human player (R or Y)
    while humanChip != "R" and humanChip != "Y":  # incorrect input color of pieces
        print("Invalid input, please try again")
        humanChip = input()                     # color of the human player (R or Y)
    global aiChip
    aiChip = "R"                 # default color of ai
    print("\nNo moves yet")
    printGameBoard(gameBoard)    # print the beining board

    if humanChip == "R":         # if human chose R (red), they go first
        aiChip = "Y"             # ai is then Y (yellow)
        humanMove(gameBoard)

    while True:                 # AI and player takes turn to move
        aiMove(gameBoard)       # ai take a turn
        # check the board for complete after the ai move
        aiWin = complete(aiChip, gameBoard)
        if aiWin == 0:         # if the ai win
            print("\n", aiChip, " wins! Game Over")
            quit()
        elif aiWin == 1:       # if the board is a draw
            print("Draw! Game Over")
            quit()

        humanMove(gameBoard)  # player take a turn
        # check the board for complete after player move
        humanWin = complete(humanChip, gameBoard)
        if humanWin == 0:  # if player win
            print("\n", humanChip, " wins! Game Over")
            quit()
        elif humanWin == 1:  # if the board is a draw
            print("Draw! Game Over")
            quit()


def minimax(board, depth, alpha, beta, maximizingPlayer):
    '''This function determine the score of a move using the minimax algorithm with alpha-beta pruning'''
    
    if maximizingPlayer:  # if the maximizing player is the ai
        chip = aiChip     # color of the ai
    else:
        chip = humanChip  # color of the player

    if depth == 0 or complete(chip, board) != 2: # check terminal
        return heuristic(chip, board)

    if maximizingPlayer:  # if true (ai turn)
        value = -1000000
        for move in getAllValidMoves(board): # for all possible moves in the board
            tempBoard = copyBoard(board) # make a copy of the board
            insert(possibleLetters[move[0]], move[1], tempBoard) # take a move from the possible moves list
            value = max(value, minimax(tempBoard, depth - 1, alpha, beta, False)) # value = next best move
            if value >= beta:  # alpha-beta pruning
                break
            alpha = max(alpha, value)
        return value
    else:  # if false (human turn)
        value = 1000000
        for move in getAllValidMoves(board): # for all possible moves in the board
            tempBoard = copyBoard(board) # make a copy of the boar
            insert(possibleLetters[move[0]], move[1], tempBoard) # take a move from the possible moves list
            value = min(value, minimax(tempBoard, depth - 1, alpha, beta, True)) # value = next best move
            if value <= alpha:  # alpha-beta pruning
                break
            beta = min(beta, value)
        return value


def isYellowTurn(board):
    '''return false if it is red turn, true if yellow'''
    
    yellowCount = 0 # count of yellow pieces on the board
    redCount = 0 # count of red pieces on the board
    for x in range(rows):  # get count of yellow and red pieces on the board
        for y in range(cols):
            if board[x][y] == "Y":
                yellowCount += 1
            elif board[x][y] == "R":
                redCount += 1

    if yellowCount < redCount:  # if there are more red, its yellow turn
        return True
    else:
        return False


def copyBoard(gameBoard):
    '''this function will return a copy of the inputted game board'''

    # create a temp board
    tempBoard = [["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E"]]
    
    for x in range(rows): # copy all values from inputted board
        for y in range(cols):
            tempBoard[x][y] = gameBoard[x][y]
    return tempBoard


def heuristic(chip, gameBoard):
    ''' this function will return a score for a inputted board state
    score will be based on how many consecutive chips are in a row: 
    +2 for 2 in a row and +5 for 3 in a row, and +100000 for wins or draws
    '''
    
    score = 0
    # Check wins horizontal spaces
    for x in range(rows):
        for y in range(cols - 3):
            if gameBoard[x][y] == chip and gameBoard[x][y+1] == chip and gameBoard[x][y+2] == chip and gameBoard[x][y+3] == chip:
                score += 100000

    # Check wins vertical spaces
    for x in range(rows - 3):
        for y in range(cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y] == chip and gameBoard[x+2][y] == chip and gameBoard[x+3][y] == chip:
                score += 100000

    # Check wins upper right to bottom left diagonal spaces
    for x in range(rows - 3):
        for y in range(3, cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y-1] == chip and gameBoard[x+2][y-2] == chip and gameBoard[x+3][y-3] == chip:
                score += 100000

    # Check wins upper left to bottom right diagonal spaces
    for x in range(rows - 3):
        for y in range(cols - 3):
            if gameBoard[x][y] == chip and gameBoard[x+1][y+1] == chip and gameBoard[x+2][y+2] == chip and gameBoard[x+3][y+3] == chip:
                score += 100000

    # check for draws
    full = True
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == "E":
                full = False
    if full:
        score += 100000

    # check 2 and 3 in a row, horizontally
    for x in range(rows):
        for y in range(cols - 1):
            if gameBoard[x][y] == chip and gameBoard[x][y+1] == chip:
                score += 2
                if y + 2 <= cols - 1:
                    if gameBoard[x][y+2] == chip:
                        score += 5

    # check 2 and 3 in a row, vertically
    for x in range(rows - 1):
        for y in range(cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y] == chip:  # 2 in a row
                score += 2
                if x + 2 <= rows - 1:
                    if gameBoard[x+2][y] == chip:  # 3 in a row
                        score += 5

    # check 2 and 3 in a row, diagonally upper right to bottom left
    for x in range(rows - 1):
        for y in range(1, cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y-1] == chip:
                score += 2
                if x + 2 <= rows - 1 and y - 2 >= 0:
                    if gameBoard[x+2][y-2] == chip:
                        score += 5

    # Check upper left to bottom right diagonal spaces
    for x in range(rows - 1):
        for y in range(cols - 1):
            if gameBoard[x][y] == chip and gameBoard[x+1][y+1] == chip:
                score += 2
                if x + 2 <= rows - 1 and y + 2 <= cols - 1:
                    if gameBoard[x+2][y+2] == chip:
                        score += 5
    return score


def getAllValidMoves(gameBoard):
    '''This function will return a list of all possible coordinates of valid moves'''
    
    allCoords = [] # list of all valid moves
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == "E": # if spot is empty then it's valid
                allCoords.append((x, y))
    return allCoords


def aiMove(gameBoard):
    '''This function make the ai move one step'''
    
    global humanChip, aiChip
    bestMove = () # the move the ai will use
    bestValue = -1000000
    for move in getAllValidMoves(gameBoard): # for each valid move, get minimax score
        tempBoard = copyBoard(gameBoard) # create a temp board
        insert(possibleLetters[move[0]], move[1], tempBoard) # take the move on the temp board
        minimaxValue = minimax(tempBoard, 3, -1000000, 1000000, True) # get the temp board minimax score
        if minimaxValue >= bestValue: # if the minimax score is better than current, switch to that move
            bestMove = (move[0], move[1])
            bestValue = minimaxValue

    # print the move the ai took
    if aiChip == "R":
        print("\nRed moves",
              possibleLetters[bestMove[0]] + "-" + str(bestMove[1] + 1) + "-n")
    elif aiChip == "Y":
        print("\nYellow moves",
              possibleLetters[bestMove[0]] + "-" + str(bestMove[1] + 1) + "-n")

    insert(possibleLetters[bestMove[0]], bestMove[1], gameBoard) # the ai take the best move
    printGameBoard(gameBoard)


def humanMove(gameBoard):
    '''This function ask what the user want to move then execute it'''
    
    global humanChip
    print("\nPlease enter your move (format row-column-flip_column):")

    userInput = [*input()]  # get input from user and put it in array form
    rightInput = False
    while not rightInput:
        if len(userInput) >= 5:  # check if user input is correct length
            if (userInput[0] in possibleLetters and userInput[1] == "-"
                    and userInput[2] in possibleNums and userInput[3] == "-"
                    and (userInput[4] == "n" or userInput[4] in possibleFlip)):  # check for valid user input
                # check if coordinate is empty
                if gameBoard[possibleLetters.index(userInput[0])][int(userInput[2]) - 1] == "E":
                    rightInput = True
        if not rightInput: # if not valid input, prompt user to retry
            print("\nInvalid input, please enter your move (format row-column-flip_column)")
            userInput = [*input()] # get input from user and put it in array form

    # insert at the location specified by user
    insert(userInput[0], int(userInput[2]) - 1, gameBoard)

    if userInput[4] != "n":  # flip at where the user specified
        flip(int(userInput[4]), gameBoard)

    # print the move the player made
    if humanChip == "R":
        print("Red moves", ''.join(userInput))
    elif humanChip == "Y":
        print("Yellow moves", ''.join(userInput))
    printGameBoard(gameBoard)


def complete(chip, gameBoard):
    '''This function will check the state of a game board for a win (0), draw (1), or incomplete (2)'''
    
    # Check wins in horizontal spaces
    for x in range(rows):
        for y in range(cols - 3):
            if gameBoard[x][y] == chip and gameBoard[x][y+1] == chip and gameBoard[x][y+2] == chip and gameBoard[x][y+3] == chip:
                return 0

    # Check wins in vertical spaces
    for x in range(rows - 3):
        for y in range(cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y] == chip and gameBoard[x+2][y] == chip and gameBoard[x+3][y] == chip:
                return 0

    # Check wins in upper right to bottom left diagonal spaces
    for x in range(rows - 3):
        for y in range(3, cols):
            if gameBoard[x][y] == chip and gameBoard[x+1][y-1] == chip and gameBoard[x+2][y-2] == chip and gameBoard[x+3][y-3] == chip:
                return 0

    # Check win in upper left to bottom right diagonal spaces
    for x in range(rows - 3):
        for y in range(cols - 3):
            if gameBoard[x][y] == chip and gameBoard[x+1][y+1] == chip and gameBoard[x+2][y+2] == chip and gameBoard[x+3][y+3] == chip:
                return 0

    # check for draws
    full = True
    for x in range(rows):
        for y in range(cols):
            if gameBoard[x][y] == "E":
                full = False
    if full:
        return 1 # board is draw
    else:
        return 2  # board is not complete


def printGameBoard(gameBoard):
    '''this function will print the given game board'''
    
    print("\n   1 2 3 4 5", end="")  # print column number
    for x in range(rows):
        print("\n  +-+-+-+-+-+")  # print separator
        print(possibleLetters[x], "|", end="")
        for y in range(cols):
            if (gameBoard[x][y] == "Y"):
                print(gameBoard[x][y], end="|")
            elif (gameBoard[x][y] == "R"):
                print(gameBoard[x][y], end="|")
            else:
                print(gameBoard[x][y], end="|")
    print("\n  +-+-+-+-+-+")


def flip(col, gameBoard):
    '''this function will flip a column of the given game board'''
    
    col = col - 1 # index of board and display is offset by one
    temp = [] # temp of the column
    for x in range(rows):  # save the reverse order of the column in a temp array
        temp.append(gameBoard[rows - x - 1][col])
    for x in range(rows):  # swap that column in gameBoard with the temp array
        gameBoard[x][col] = temp[x]


def insert(x, y, gameBoard):
    '''This function insert the piece at the input location'''
    
    x = possibleLetters.index(x)  # get the index of the inputted letter

    yellowTurn = isYellowTurn(gameBoard)
    if gameBoard[x][y] != "E":  # make sure spot is not taken
        return False
    else:
        if yellowTurn:  # if yellow's turn insert Y
            gameBoard[x][y] = "Y"
        else:  # if yellow's turn insert R
            gameBoard[x][y] = "R"
    return True


main()
