'''
Created on Apr 18, 2013
@author: Matt, Arjun
'''
from copy import deepcopy
import Queue
from time import time
from sets import Set

global timeTaken

# FIX THIS TO NOT USE BOARD ONCE I FIX OTHER ONES
def solve(board, cars):
    global timeTaken
    x = 0
    timeTaken = 0
    x -= time()
    init = makeArray(board)
    q = Queue.Queue()
    seen = Set()
    p = ()
    q.put((init, p))
    solFound = False
    
    while q.qsize() != 0 and solFound == False:
        curFull = q.get()
        cur = curFull[0]
        if checkForWin(board.master.winrow, cur):
            solFound = True
            solution = curFull
            break
        mvs = getAllMoves(cars, cur)                    # 1.06s on 1, 4.23s on 35, 30.3s on 50 (all multi-length)
                                                        # 0.81s on 1, 3.57s on 35, 23.4s on 50(all 1-length)
        for mvKey in mvs:                               # 0.34s on 1, 3.87s on 35, 24.65s on insane (all multi-length)
                                                        # 0.43s on 1, 5.85s on 35, 58.84s on insane (all 1-length)
            for mv in mvs[mvKey]:
                if str(mv) not in seen:
#                     timeTaken -= time()
#                     prev = deepcopy(curFull)    #deepcopy necessary?    MOST TIME SPENT HERE!!! >95% of search time.
                    prev = curFull
#                     timeTaken += time()
                    seen.add(str(mv))
                    q.put((mv, prev))
    x += time()
    print "Total time solving: " + str(x)
    print "Total time deepcopying: " + str(timeTaken)
    return solution
    
# OK TO USE BOARD!
def makeArray(board):
    boardString = [["X" for x in range(board.master.rows)] for y in range(board.master.columns)]
    xx = 0
    yy = 0
    for car in board.master.carArray:
        if board.master.carArray[car].direction == "vert":
            i = 0
            while i < board.master.carArray[car].length:
                xx = board.master.carArray[car].xmin/board.master.cellwidth
                yy = board.master.carArray[car].ymin/board.master.cellheight + i
                boardString[xx][yy] = board.master.carArray[car].name
                i += 1
        else: # "horiz"
            i = 0
            while i < board.master.carArray[car].length:
                xx = board.master.carArray[car].xmin/board.master.cellwidth + i
                yy = board.master.carArray[car].ymin/board.master.cellheight
                boardString[xx][yy] = board.master.carArray[car].name
                i += 1
    return boardString
    
# OK FOR THIS TO USE BOARD
def updateBoard(board, boardString):
    x = 0
    y = 0
    carArray = board.master.carArray
    for car in board.master.carArray:
        found = False
        x = 0
        y = 0
        for column in range(board.master.columns):
            if found:
                break
            y = 0
            for row in range(board.master.rows):
                if found:
                    break
                if boardString[column][row] == board.master.carArray[car].name:
                    carArray[car].xmin = x
                    carArray[car].ymin = y
                    if board.master.carArray[car].direction == "vert":
                        carArray[car].xmax = x + board.master.cellwidth
                        carArray[car].ymax = y + board.master.carArray[car].length*board.master.cellheight
                    else: # "horiz"
                        carArray[car].xmax = x + board.master.carArray[car].length*board.master.cellwidth
                        carArray[car].ymax = y + board.master.cellheight
                    found = True
                y += board.master.cellheight
            x += board.master.cellwidth
#     return carArray

def movePos(boardString, carName, length):
    found = False
    startX, startY, finalX, finalY = 0, 0, 0, 0
    for column in range(len(boardString[0])):
        for row in range(len(boardString)):
            if boardString[column][row] == carName:
                if not found:
                    startX = column
                    startY = row
                    found = True
                finalX = column
                finalY = row
    if found and finalY - startY > finalX - startX and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # vert
        if finalY + length >= len(boardString[0]) or boardString[finalX][finalY + length] != "X":   # Number of rows
            return False
        for space in range(length):
            boardString[startX][startY + space] = "X"
            boardString[finalX][finalY + space + 1] = carName
         
    elif found and finalX - startX > finalY - startY and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # "horiz"
        if finalX + length >= len(boardString) or boardString[finalX + length][finalY] != "X": # Number of columns
            return False
        for space in range(length):
            boardString[startX + space][startY] = "X"
            boardString[finalX + space + 1][finalY] = carName
    if not found:
        return False
    return boardString

def moveNeg(boardString, carName, length):
    found = False
    startX, startY, finalX, finalY = 0, 0, 0, 0
    for column in range(len(boardString[0])):
        for row in range(len(boardString)):
            if boardString[column][row] == carName:
                if not found:
                    startX = column
                    startY = row
                    found = True
                finalX = column
                finalY = row
    if found and finalY - startY > finalX - startX and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # vert
        if startY - length < 0 or boardString[startX][startY - length] != "X":   # Number of rows
            return False
        for space in range(length):
            boardString[finalX][finalY - space] = "X"
            boardString[startX][startY - space - 1] = carName
        
    elif found and finalX - startX > finalY - startY and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # "horiz"
        if startX - length < 0 or boardString[startX - length][startY] != "X": # Number of columns
            return False
        for space in range(length):
            boardString[finalX - space][finalY] = "X"
            boardString[startX - space - 1][startY] = carName
    if not found:
        return False
    return boardString

def getAllMoves(cars, boardString):
    global timeTaken
    moves = {}
    for car in cars:
        moves[car] = []
        timeTaken -= time()
        newBrdStr = deepcopy(boardString)
        timeTaken += time()

        for length in range(len(boardString)):              # Uncomment this line to do any length moves
#         for length in range(2):                           # Uncomment this line to do only moves of length 1
            if length == 0:
                continue
            if movePos(newBrdStr, car, length) != False:
                moves[car].append(newBrdStr)
                timeTaken -= time()
                newBrdStr = deepcopy(boardString)
                timeTaken += time()
            else:
                break
        for length in range(len(boardString)):              # Uncomment this line to do any length moves
#         for length in range(2):                           # Uncomment this line to do only moves of length 1
            if length == 0:
                continue
            if moveNeg(newBrdStr, car, length) != False:
                moves[car].append(newBrdStr)
                timeTaken -= time()
                newBrdStr = deepcopy(boardString)
                timeTaken += time()
            else:
                break
    return moves

def checkForWin(winrow, boardString):
    for column in range(len(boardString[0])):
        for row in range(len(boardString)):
            if boardString[column][row] == "Goal":
                if column == len(boardString[0]) - 1 and row == winrow:
                    return True
    return False

# OK TO USE BOARD
def getCarArray(board):
    cars = []
    for car in board.master.carArray:
        cars.append(board.master.carArray[car].name)
    return cars