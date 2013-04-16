'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
from random import randrange
import tkMessageBox
import winsound
import threading
# from sys import argv
# import time

global currentCar
currentCar = None

global moved  # Checks if a move was made, for use in 
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

        master.level = StringVar()
        master.level.set("Level 1 - Beginner")
        master.menu = OptionMenu(master, master.level, "Level 1 - Beginner", \
            "Level 2 - Beginner", "Level 3 - Beginner", "Level 4 - Beginner", "Level 5 - Beginner", \
            "Level 11 - Intermediate", "Level 12 - Intermediate", "Level 13 - Intermediate", "Level 14 - Intermediate", "Level 15 - Intermediate", \
            "Level 21 - Advanced", "Level 22 - Advanced", "Level 23 - Advanced", "Level 24 - Advanced", "Level 25 - Advanced", \
            "Level 31 - Expert", "Level 32 - Expert", "Level 33 - Expert", "Level 34 - Expert", "Level 35 - Expert", \
            "Level 41 - Insane", "Level 42 - Insane", "Level 43 - Insane", "Level 44 - Insane", "Level 45 - Insane", \
            "Level 46 - Insane", "Level 47 - Insane", "Level 48 - Insane", "Level 49 - Insane", "Level 50 - Insane", \
            "Level 51 - Insane", "Level 52 - Insane", "Level 53 - Insane", "Level 54 - Insane", "Level 55 - Insane", \
            "Level 56 - Insane", "Level 57 - Insane", "Level 58 - Insane", "Level 59 - Insane", "Level 60 - Insane", \
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
        
        master.movesLbl = Label(master, text="Total moves: " + str(master.moves))
        master.movesLbl.place(x=620, y=200, height=40, width=160)
        
        master.remainingLbl = Label(master, text="Minimum moves\n remaining: " + str(self.remaining()))
        master.remainingLbl.place(x=620, y=260, height=40, width=160)
        
        self.reset()
        master.canvas.bind("<Button-1>", self.mousePressed)
        master.canvas.bind("<Key>", self.keyPressed)

    def nextMove(self):
        print "Next move pressed!"
        
    def solve(self):
        print "Solve pressed!"
        
    def generate(self):
        print "Generate pressed!"
        
    def remaining(self):
        return randrange(0, 10)

    def reset(self):  # This method takes no parameters (for button).
        self.resetEvent(None)

    def resetEvent(self, event):  # This method takes a parameter (for optionmenu)
        self.master.carArray = {}  # Stores all our cars that are on the board
        self.master.rect = {}  # Stores all the rectangles (grid).
        self.clearBoard()
        self.drawGrid()
        self.loadCars()
        self.drawCars()
        self.master.moves = -1  # Resets moves to 0
        self.incrementMoves()
        
    def incrementMoves(self):
        self.master.moves += 1
        self.master.movesLbl = Label(self.master, text="Total moves: " + str(self.master.moves))
        self.master.movesLbl.place(x=620, y=200, height=80, width=180)
        self.master.remainingLbl = Label(self.master, text="Minimum moves\n remaining: " + str(self.remaining()))
        self.master.remainingLbl.place(x=620, y=260, height=40, width=160)

    def keyPressed(self, event):
        global moved
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
        global currentCar
        if event.char == 'r':
            self.reset()  # Will make this a physical button at some point
            return
        
        if currentCar != None:
            if currentCar.direction == 'vert':
                if event.char == 'w':
                    currentCar.move(0, -1 * self.master.cellheight)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.ymax > self.master.columns * self.master.cellheight) or (currentCar.ymin < 0):
                        currentCar.move(0, 1 * self.master.cellheight)                        
                if event.char == 's':
                    currentCar.move(0, 1 * self.master.cellheight)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.ymax > self.master.columns * self.master.cellheight) or (currentCar.ymin < 0):
                        currentCar.move(0, -1 * self.master.cellheight)
            if currentCar.direction == 'horiz':
                if event.char == 'a':
                    currentCar.move(-1 * self.master.cellwidth, 0)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.xmax > self.master.columns * self.master.cellwidth) or (currentCar.xmin < 0):
                        currentCar.move(1 * self.master.cellwidth, 0)
                if event.char == 'd':
                    currentCar.move(1 * self.master.cellwidth, 0)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.xmax > self.master.columns * self.master.cellwidth) or (currentCar.xmin < 0):
                        currentCar.move(-1 * self.master.cellwidth, 0)
            moved = True
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
        self.checkForWin()
      
    def mousePressed(self, event):
        global currentCar, moved
#         print "Hi!"
        if moved:
            self.incrementMoves()
            moved = False
        currentCar = None
        for index in self.master.carArray:
            self.master.carArray[index].tags = 'car'  # Do this to un-highlight all non-current cars
            if event.x > self.master.carArray[index].xmin and event.x < self.master.carArray[index].xmax and event.y > self.master.carArray[index].ymin and event.y < self.master.carArray[index].ymax:
                currentCar = self.master.carArray[index]
                currentCar.tags = 'current'
                # Save old car (duplicate, not reference) in case it screws up later.
                # WHY WONT YOU WORK !
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
#                 return    # Doesn't uncolor all cars right if I return early.
    
    def checkForWin(self):
        for i in self.master.carArray:
            car = self.master.carArray[i]
            if car.xmax >= self.master.columns * self.master.cellwidth and car.ymin == self.master.winrow * self.master.cellheight and car.direction == 'horiz':
                winBox = tkMessageBox.showinfo("Win Message", "Congratulations, you won!")
                self.reset()
                threading.Thread(target=winsound.PlaySound('fanfare.wav', winsound.SND_FILENAME)).start()            

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
                self.master.carArray[index].draw(self.master)

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
            temp = Car(self.master, splitLine[0], (int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]))
            self.master.carArray[splitLine[0]] = temp
            
    def clearBoard(self):
        self.master.canvas.delete(ALL)
    
class Car(object):
    # construtor
    xmin, xmax, ymin, ymax, color, direction, tags = 0, 0, 0, 0, "", "", ""
    def __init__(self, master, name, xmin, ymin, xmax, ymax):
        self.length = max(xmax - xmin, ymax - ymin)
        self.xmin = xmin * master.cellwidth
        self.ymin = ymin * master.cellheight
        self.xmax = xmax * master.cellwidth
        self.ymax = ymax * master.cellheight
        self.color = "red" if name == "Goal" else "#%06s" % "".join([hex(randrange(16, 255))[2:] for i in range(3)])  #  Most elegant line of code I've ever written.
        self.direction = "horiz" if self.xmax - self.xmin > self.ymax - self.ymin else "vert"
    
    # draws a car on the board
    def draw(self, master):
        if self.tags == 'current':
            master.rect[self.xmin, self.ymin] = master.canvas.create_rectangle(self.xmin + 5, self.ymin + 5, self.xmax - 5, self.ymax - 5, fill=self.color, tags=self.tags, outline='black', width=5)
        else:
            master.rect[self.xmin, self.ymin] = master.canvas.create_rectangle(self.xmin + 5, self.ymin + 5, self.xmax - 5, self.ymax - 5, fill=self.color, tags=self.tags)
       
    # checks if two cars are colliding
    def isColliding(self, car2):
        if ((self.xmin >= car2.xmin and self.xmin < car2.xmax) and (self.ymin >= car2.ymin and self.ymin < car2.ymax)) \
            or ((self.xmax > car2.xmin and self.xmax <= car2.xmax) and (self.ymax > car2.ymin and self.ymax <= car2.ymax)):
            return True
        return False
                
    # moves a car somewhere else
    def move(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
        
    def checkForCollisions(self, master):
        for i in master.carArray:
            car2 = master.carArray[i]
            if self != car2 and self.isColliding(car2):
                return True
        return False
           
def main():
    root = Tk()
    root.geometry('800x600+0+0')  # Make this be parameters + buffer space
    thingy = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()
