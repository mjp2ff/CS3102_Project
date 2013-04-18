'''
Created on Apr 18, 2013

@author: Matt
'''
from copy import deepcopy
import Queue

def solve(board):
    init = makeArray(board)
    q = Queue.Queue()
    seen = []
    q.put(init)
    solFound = False
        
    while q.qsize() != 0 and solFound == False:
        cur = q.get()
#         print len(seen)
        solution = cur
        if checkForWin(board, cur):
            solFound = True
            solution = cur
            break
        mvs = getAllMoves(board, cur)
        for mvKey in mvs:
            for mv in mvs[mvKey]:
                if mv not in seen:
                    seen.append(mv)
                    q.put(mv)
    
    return makeBoard(board, solution)
    
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
    
def makeBoard(board, boardString):
    x = 0
    y = 0
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
                    board.master.carArray[car].xmin = x
                    board.master.carArray[car].ymin = y
                    if board.master.carArray[car].direction == "vert":
                        board.master.carArray[car].xmax = x + board.master.cellwidth
                        board.master.carArray[car].ymax = y + board.master.carArray[car].length*board.master.cellheight
                    else: # "horiz"
                        board.master.carArray[car].xmax = x + board.master.carArray[car].length*board.master.cellwidth
                        board.master.carArray[car].ymax = y + board.master.cellheight
                    found = True
                y += board.master.cellheight
            x += board.master.cellwidth
    return board

def movePos(boardString, carName):
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
        if finalY + 1 >= len(boardString[0]) or boardString[finalX][finalY+1] != "X":   # Number of rows
            return False
        boardString[startX][startY] = "X"
        boardString[finalX][finalY+1] = carName
#         
    elif found and finalX - startX > finalY - startY and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # "horiz"
        if finalX + 1 >= len(boardString) or boardString[finalX+1][finalY] != "X": # Number of columns
            return False
        boardString[startX][startY] = "X"
        boardString[finalX+1][finalY] = carName
    return boardString

def moveNeg(boardString, carName):
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
        if startY - 1 < 0 or boardString[startX][startY-1] != "X":   # Number of rows
            return False
        boardString[finalX][finalY] = "X"
        boardString[startX][startY-1] = carName
        
    elif found and finalX - startX > finalY - startY and boardString[startX][startY] == carName and boardString[finalX][finalY] == carName: # "horiz"
        if startX - 1 < 0 or boardString[startX-1][startY] != "X": # Number of columns
            return False
        boardString[finalX][finalY] = "X"
        boardString[startX-1][startY] = carName
    return boardString

def getAllMoves(board, boardString):
    moves = {}
    for car in board.master.carArray:
        moves[board.master.carArray[car].name] = []
        newBrdStr = deepcopy(boardString)
        if movePos(newBrdStr, board.master.carArray[car].name) != False:
            moves[board.master.carArray[car].name].append(newBrdStr)
        newBrdStr = deepcopy(boardString)
        if moveNeg(newBrdStr, board.master.carArray[car].name) != False:
            moves[board.master.carArray[car].name].append(newBrdStr)
    return moves

def checkForWin(board, boardString):
    for column in range(len(boardString[0])):
        for row in range(len(boardString)):
            if boardString[column][row] == "Goal":
                if column == len(boardString[0]) - 1 and row == board.master.winrow:
                    return True
    return False