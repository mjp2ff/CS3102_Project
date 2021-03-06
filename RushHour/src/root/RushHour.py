'''
Created on Apr 9, 2013
@author: Matt, Arjun
'''
from Tkinter import *
from random import randrange, sample
import tkMessageBox
import winsound
from time import sleep, clock, time
import Solver

global currentCar
currentCar = None

global moved
moved = False

class Board:
    master = None
    def __init__(self, master):        
        self.master = master
        master.canvas = Canvas(master, width=600, height=600, borderwidth=0, highlightthickness=0)
        master.canvas.pack(side="left", fill="both", expand="true")
        master.canvas.focus_set()
       
        master.rows = 6
        master.columns = 6
        master.winrow = 2
        master.wincolumn = 5
        master.cellwidth = (int)(master.canvas.cget('width')) / master.columns
        master.cellheight = (int)(master.canvas.cget('height')) / master.rows
        master.moves = 0
        
        self.master.carArray = {}   # Stores all our cars that are on the board
        self.master.rect = {}       # Stores all the rectangles (grid).
        self.master.movesDone = []  # Stores all the moves done up to this point on the board.

        master.level = StringVar()
        master.level.set("Level 1 - Beginner")
        master.menu = OptionMenu(master, master.level, "Level 1 - Beginner", \
            "Level 2 - Beginner", "Level 3 - Beginner", "Level 4 - Beginner", "Level 5 - Beginner", \
            "Level 11 - Intermediate", "Level 12 - Intermediate", "Level 13 - Intermediate", "Level 14 - Intermediate", "Level 15 - Intermediate", \
            "Level 21 - Advanced", "Level 22 - Advanced", "Level 23 - Advanced", "Level 24 - Advanced", "Level 25 - Advanced", \
            "Level 31 - Expert", "Level 32 - Expert", "Level 33 - Expert", "Level 34 - Expert", "Level 35 - Expert", \
            "Level 41 - Insane", "Level 42 - Insane", "Level 43 - Insane", "Level 44 - Insane", "Level 45 - Insane", \
            "Level 46 - Insane", "Level 47 - Insane", "Level 48 - Insane", "Level 49 - Insane", "Level 50 - Insane", \
            command=self.resetEvent)
#         master.menu.pack(side="top", fill=X)
        master.menu.place(x=610, y=10, height=80, width=180)
        
        master.resetButton = Button(master, text="RESET", command=self.reset)
        master.resetButton.place(x=610, y=110, height=80, width=180)

        master.nextMoveButton = Button(master, text="Make next move", command=self.nextMove)
        master.nextMoveButton.place(x=610, y=310, height=80, width=180)
                
        master.solveButton = Button(master, text="Solve puzzle", command=self.solve)
        master.solveButton.place(x=610, y=410, height=80, width=180)
        
        master.generateButton = Button(master, text="Generate puzzle", command=self.generate)
        master.generateButton.place(x=610, y=510, height=80, width=180)
        
        master.movesLbl = Label(master, text="Total moves: " + str(self.master.moves))
        master.movesLbl.place(x=620, y=215, height=40, width=160)
        
        self.reset()
        master.canvas.bind("<Button-1>", self.mousePressed)
        master.canvas.bind("<Key>", self.keyPressed)

    def nextMove(self):
        nextMove(self)
        
    def solve(self):
        solve(self)
        
    def generate(self):
        generate(self)  # Call real generate method

    def reset(self):  # This method takes no parameters (for button).
        self.resetEvent(None)

    def resetEvent(self, event):  # This method takes a parameter (for optionmenu)
        global moved
        self.master.carArray = {}  # Stores all our cars that are on the board
        self.master.rect = {}  # Stores all the rectangles (grid)
        self.master.movesDone = []
        self.master.moves = 0
        moved = False
        self.clearBoard()
        self.drawGrid()
        self.loadCars()
        self.drawCars()
        self.master.movesLbl.destroy()
        self.master.movesLbl = Label(self.master, text="Total moves: " + str(0))
        self.master.movesLbl.place(x=620, y=215, height=80, width=180)
        
    def incrementMoves(self):
        self.master.moves += 1
        self.master.movesLbl.destroy()
        self.master.movesLbl = Label(self.master, text="Total moves: " + str(self.master.moves))
        self.master.movesLbl.place(x=620, y=215, height=80, width=180)

    def keyPressed(self, event):
        global currentCar, moved
        self.clearBoard()
        self.drawGrid()
        self.drawCars()  
        if currentCar != None:
            m = None
            if currentCar.direction == 'vert':
                if event.char == 'w':
                    m = Move(currentCar, -1)      
                if event.char == 's':
                    m = Move(currentCar, 1)
            if currentCar.direction == 'horiz':
                if event.char == 'a':
                    m = Move(currentCar, -1)
                if event.char == 'd':
                    m = Move(currentCar, 1)
            if m != None:
                m.currentCar.doMove(m)
                if m.currentCar.validateMove(m):
                    moved = True
                else:
                    moved = False
            else:
                moved = False
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
        self.checkForWin()
      
    def mousePressed(self, event):
        global currentCar, moved
        currentCar = None
        for index in self.master.carArray:
            self.master.carArray[index].tags = 'car'  # Do this to un-highlight all non-current cars
            if event.x > self.master.carArray[index].xmin and event.x < self.master.carArray[index].xmax and event.y > self.master.carArray[index].ymin and event.y < self.master.carArray[index].ymax:
                currentCar = self.master.carArray[index]
                currentCar.tags = 'current'
                if moved:
                    self.incrementMoves()
                    moved = False
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
#                 return    # Doesn't uncolor all cars right if I return early.
    
    def checkForWin(self):
        for i in self.master.carArray:
            car = self.master.carArray[i]
            if car.xmax >= self.master.columns * self.master.cellwidth and car.ymin == self.master.winrow * self.master.cellheight and car.direction == 'horiz':
                winBox = tkMessageBox.showinfo("Win Message", "Congratulations! You took: " + str(self.master.moves) + " moves.")
                if (self.master.level.get() == "SolvedBoard"):
                    self.master.level.set("Level 1 - Beginner")
                self.reset()
                target=winsound.PlaySound('fanfare.wav', winsound.SND_FILENAME)

    def drawGrid(self):
        for column in range(self.master.columns):
            for row in range(self.master.rows):
                x1 = column * self.master.cellwidth
                y1 = row * self.master.cellheight
                x2 = x1 + self.master.cellwidth
                y2 = y1 + self.master.cellheight
                self.master.rect[row, column] = self.master.canvas.create_rectangle(x1, y1, x2, y2, fill="white", tags="grid")
                if column == self.master.wincolumn and row == self.master.winrow:
                    self.master.rect[row, column + 1] = self.master.canvas.create_rectangle(x2, y1, x2 + (x2 - x1) / 10, y2, fill="orangered", tags="grid")  # Maybe change tags later?
                    # ONLY WORKS IF YOU EXIT TO THE RIGHT        

    def drawCars(self):  # master is board
        # There are no initial collisions, so draw for real
        for index in self.master.carArray:
            if self.master.carArray[index] != None:
                self.master.carArray[index].draw()

    def loadCars(self):
        # read in the lines from the file
        # script, filename = argv                # FIX THIS LATER
        with open(self.master.level.get()) as f:
            content = f.readlines()
        
        # load in each car in the file
        for line in content:
            splitLine = line.split(" ")
            initCoords = splitLine[1].split(",")
            endCoords = splitLine[2].split(",")
            temp = Car(self, splitLine[0], (int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]))
            self.master.carArray[splitLine[0]] = temp
            
    def clearBoard(self):
        self.master.canvas.delete(ALL)
    
    # Generates a valid move.
    def generateMove(self):
        while True:
            randCarArray = sample(self.master.carArray, 1)
            randCar = self.master.carArray[randCarArray[0]]
            tempMove = Move(randCar, randrange(-1, 2, 1))
            if randCar.checkMove(tempMove) and tempMove.dist != 0:
                return tempMove
    
    #Checks board for collisions.            
    def checkForCollisions(self, carArray):
        for i in carArray:
            car1 = carArray[i]
            for j in carArray:
                car2 = carArray[j]
                if car1 != car2 and car1.isColliding(car2):
                    return True
        return False
            
class Car(object):
    master, xmin, xmax, ymin, ymax, color, direction, tags = None, 0, 0, 0, 0, "", "", ""
    # constructor
    def __init__(self, board, name, xmin, ymin, xmax, ymax):
        self.board = board
        self.name = name
        self.length = max(xmax - xmin, ymax - ymin)
        self.xmin = xmin * board.master.cellwidth
        self.ymin = ymin * board.master.cellheight
        self.xmax = xmax * board.master.cellwidth
        self.ymax = ymax * board.master.cellheight
        self.color = "red" if name == "Goal" else "#%06s" % "".join([hex(randrange(16, 255))[2:] for i in range(3)])  #  Most elegant line of code I've ever written.
        self.direction = "horiz" if self.xmax - self.xmin > self.ymax - self.ymin else "vert"
    
    # draws a car on the board
    def draw(self):
        if self.tags == 'current':
            self.board.master.rect[self.xmin, self.ymin] = self.board.master.canvas.create_rectangle(self.xmin + 5, self.ymin + 5, self.xmax - 5, self.ymax - 5, fill=self.color, tags=self.tags, outline='black', width=5)
        else:
            self.board.master.rect[self.xmin, self.ymin] = self.board.master.canvas.create_rectangle(self.xmin + 5, self.ymin + 5, self.xmax - 5, self.ymax - 5, fill=self.color, tags=self.tags)
       
    # checks if two cars are colliding
    def isColliding(self, car2):
        if ((self.xmin >= car2.xmin and self.xmin < car2.xmax) and (self.ymin >= car2.ymin and self.ymin < car2.ymax)) \
            or ((self.xmax > car2.xmin and self.xmax <= car2.xmax) and (self.ymax > car2.ymin and self.ymax <= car2.ymax)):
            return True
        return False
    
    # Checks if a made move was valid. If it wasn't it reverses that move. DOES NOT ADD IT TO MOVESDONE ANYMORE
    def validateMove(self, move):
        if (self.board.checkForCollisions(self.board.master.carArray)) or (self.ymax > self.board.master.columns * self.board.master.cellheight) or (self.ymin < 0) \
            or (self.xmax > self.board.master.columns * self.board.master.cellwidth) or (self.xmin < 0):
            self.doMove(Move(move.currentCar, -1 * move.dist))
            return False
        else:
            return True
        
    # Checks whether a potential move would be valid. Changes nothing.
    def checkMove(self, move):
        self.doMove(move)
        good = True
        if (self.board.checkForCollisions(self.board.master.carArray)) or (self.ymax > self.board.master.columns * self.board.master.cellheight) or (self.ymin < 0) \
            or (self.xmax > self.board.master.columns * self.board.master.cellwidth) or (self.xmin < 0):
            good = False
        self.doMove(move.getOpposite())
        return good
    
    # Moves a car somewhere else. DOES NOT CHECK FOR VALIDITY
    def doMove(self, move):
        if self.direction == "vert":
            self.ymin += move.dist*self.board.master.cellheight
            self.ymax += move.dist*self.board.master.cellheight
        elif self.direction == "horiz":
            self.xmin += move.dist*self.board.master.cellwidth
            self.xmax += move.dist*self.board.master.cellwidth
    
class Move(object):
    currentCar, dist = None, 0
    # constructor
    def __init__(self, currentCar, dist):
        self.currentCar = currentCar
        self.dist = dist
        
    def getOpposite(self):
        reverse = Move(self.currentCar, -1*self.dist)
        return reverse
        
class Node(object):
    carArray, strval, movesDone = None, "", None
    def __init__(self, carArray, movesDone):
        self.carArray = carArray
        for index in self.carArray:
            self.strval += str(self.carArray[index].xmin) + " " + str(self.carArray[index].xmax) + " " + str(self.carArray[index].ymin) + " " + str(self.carArray[index].ymax)
        self.movesDone = movesDone
        
    def same(self, node2):
        return self.strval == node2.strval
        return True

def deepCopyNode(aNode):
    cars = {}
    moves = []
    for index in aNode.carArray:
        cars[index] = aNode.carArray[index]
    for move in aNode.movesDone:
        moves.append(deepCopyMove(move))
    copy = Node(cars, moves)
    return copy

def deepCopyCar(aCar):
    copy = Car(aCar.board, aCar.name, aCar.xmin/aCar.board.master.cellwidth, aCar.ymin/aCar.board.master.cellheight, aCar.xmax/aCar.board.master.cellwidth, aCar.ymax/aCar.board.master.cellheight)
    return copy

def deepCopyMove(aMove):
    copy = Move(aMove.currentCar, aMove.dist)
    return copy

def findMove(carArray1, carArray2):
    mv = None
    for index in carArray1:
        if carArray1[index].xmin != carArray2[index].xmin:
            mv = Move(carArray1[index], carArray2[index].xmin - carArray1[index].xmin)
        if carArray1[index].ymin != carArray2[index].ymin:
            mv = Move(carArray1[index], carArray2[index].ymin - carArray1[index].ymin)
    return mv

def solve(board):
    cars = Solver.getCarArray(board)
    solution = Solver.solve(board, cars)
    
    mvs = []
    mvs.append(solution[0])
    while solution[1] != ():
        solution = solution[1]
        mvs.append(solution[0])
        
    mvs.pop()                   # Get rid of first move (no change).
    while len(mvs) != 0:
        board.incrementMoves()
        Solver.updateBoard(board, mvs.pop())
        board.clearBoard()
        board.drawGrid()
        board.drawCars()
        board.master.update()
        sleep(0.3)
    board.checkForWin()

def nextMove(board):
    cars = Solver.getCarArray(board)
    solution = Solver.solve(board, cars)
    
    mvs = []
    mvs.append(solution[0])
    while solution[1] != ():
        solution = solution[1]
        mvs.append(solution[0])
    board.incrementMoves()
    mvs.pop()           # Get rid of first move (no change).
    Solver.updateBoard(board, mvs.pop())
    board.clearBoard()
    board.drawGrid()
    board.drawCars()
    board.master.update()
    board.checkForWin()

def generate(board):                 # Takes in a board as a parameter
    board.master.level.set("SolvedBoard")
    board.reset()
    seenNodes = []
    curNode = Node(board.master.carArray, board.master.movesDone)
    seenNodes.append(curNode)
    wrong = False
    k = 0
    numTries = 0
    while k < 1000:   # Do 10 random moves
        nextMove = board.generateMove()
        nextMove.currentCar.doMove(nextMove)
        curNode = Node(board.master.carArray, board.master.movesDone)
        for n in seenNodes:
            if curNode.same(n):
                nextMove.currentCar.doMove(nextMove.getOpposite())
                wrong = True
                numTries += 1
        if not wrong:
            numTries = 0
            seenNodes.append(curNode)
            k += 1
        if numTries > 10:
            board.master.level.set("SolvedBoard")
            board.reset()
            seenNodes = []
            curNode = Node(board.master.carArray, board.master.movesDone)
            seenNodes.append(curNode)
            k = 0
            numTries = 0
        wrong = False
    board.clearBoard()
    board.drawGrid()
    board.drawCars()

def main():
    root = Tk()
    root.geometry('800x600+0+0')  # Make this be parameters + buffer space
    thingy = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()
