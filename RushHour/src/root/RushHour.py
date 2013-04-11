'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
from sys import argv
import time

global x, y, first      # globals for mouse movement
x = 0
y = 0
first = True

global currentCar, oldCar
currentCar = None
oldCar = None

class Board:
    master = None
    def __init__(self, master):
        self.master = master
        master.canvas = Canvas(master, width=600, height=600, borderwidth=0, highlightthickness=0)
        master.canvas.pack(side="top", fill="both", expand="true")
        master.rows = 6
        master.columns = 6
        master.winrow = 2
        master.cellwidth = (int)(master.canvas.cget('width')) / master.columns
        master.cellheight = (int)(master.canvas.cget('height')) / master.rows
        
        master.carArray = {}        # Stores all our cars that are on the board
        master.rect = {}            # Stores all the rectangles (grid).

        drawGrid(master)
        loadCars(master)
        drawCars(master)
        master.canvas.bind("<Button-1>", self.mousePressed)
        master.canvas.bind("<B1-Motion>", self.mouseHeld)
        master.canvas.bind("<ButtonRelease-1>", self.mouseReleased)

    def mousePressed(self, event):
        global currentCar, oldCar
#         print "Hi!"
        currentCar = None
        oldCar = None
        for index in self.master.carArray:
            if event.x > self.master.carArray[index].xmin and event.x < self.master.carArray[index].xmax and event.y > self.master.carArray[index].ymin and event.y < self.master.carArray[index].ymax:
                currentCar = self.master.carArray[index]
                # Save old car (duplicate, not reference) in case it screws up later.
                # WHY WONT YOU WORK !
                oldCar = Car(self.master, self.master.carArray[index].xmin, self.master.carArray[index].ymin, self.master.carArray[index].xmax, self.master.carArray[index].ymax, self.master.carArray[index].color, self.master.carArray[index].direction)
                return

    def mouseHeld(self, event):        
        global x, y, first, currentCar
        
        if currentCar == None:      # If not clicking on a car, return
            return 
        if first:                   # If this is the first click, return. Not sure if I need this...
            first = False
            x = event.x
            y = event.y
            return
                
        if event.x > currentCar.xmin and event.x < currentCar.xmax and event.y > currentCar.ymin and event.y < currentCar.ymax:
            if currentCar.direction == 'vert':
                if not (checkForCollisions(currentCar, self.master)) and not (currentCar.ymax > self.master.columns*self.master.cellheight) and not (currentCar.ymin < 0):
                    currentCar.move(0, event.y-y)
                if checkForWin(self.master):
                    print "You win!"
            if currentCar.direction == 'horiz':
                if not (checkForCollisions(currentCar, self.master)) and not (currentCar.xmax > self.master.columns*self.master.cellwidth) and not (currentCar.xmin < 0):
                    currentCar.move(event.x-x, 0)
                if checkForWin(self.master):
                    print "You win!"
        drawGrid(self.master)
        drawCars(self.master)
                
        x = event.x
        y = event.y
        
    def mouseReleased(self, event):      
        global first, currentCar, oldCar
        if currentCar == None:
            return      
        first = True
        if currentCar.direction == 'vert':
            dy = 0
            if currentCar.ymin < 0:
                dy = -1*(int)(currentCar.ymin)
            if currentCar.ymin > self.master.cellheight*self.master.rows:
                dy = -1*(int)(currentCar.ymin - self.master.cellheight*self.master.rows)
            if self.master.cellheight - currentCar.ymin % self.master.cellheight < currentCar.ymin % self.master.cellheight:
                dy = self.master.cellheight - currentCar.ymin % self.master.cellheight
            else:
                dy = -1*(int)(currentCar.ymin % self.master.cellheight)
            currentCar.move(0, dy)
            if (checkForCollisions(currentCar, self.master)):
                self.master.carArray[self.master.carArray.get(currentCar)] = oldCar
        elif currentCar.direction == 'horiz':
            dx = 0
            if currentCar.xmin < 0:
                dx = -1*(int)(currentCar.xmin)
            if currentCar.ymin > self.master.cellheight*self.master.rows:
                dx = -1*(int)(currentCar.xmin - self.master.cellwidth*self.master.columns)
            if self.master.cellwidth - currentCar.xmin % self.master.cellwidth < currentCar.xmin % self.master.cellwidth:
                dx = self.master.cellwidth - currentCar.xmin % self.master.cellwidth
            else:
                dx = -1*(int)(currentCar.xmin % self.master.cellwidth)
            currentCar.move(dx, 0)
            if (checkForCollisions(currentCar, self.master)):
                print "NOOOOO"
                self.master.carArray[self.master.carArray.get(currentCar)] = oldCar
        currentCar = None
        drawGrid(self.master)
        drawCars(self.master)

def checkForWin(master):
    for i in master.carArray:
        if master.carArray[i].isWin(master):
            return True
    return False

def checkAllForCollisions(master):
    for i in master.carArray:
        car1 = master.carArray[i]
        for j in master.carArray:
            car2 = master.carArray[j]
            if car1 != car2 and car1.isColliding(car2):
                return True
    return False

def checkForCollisions(car, master):
    for i in master.carArray:
        car2 = master.carArray[i]
        if car != car2 and car.isColliding(car2):
            return True
    return False
     
def drawGrid(master):
    for column in range(master.columns):
        for row in range(master.rows):
            x1 = column*master.cellwidth
            y1 = row*master.cellheight
            x2 = x1 + master.cellwidth
            y2 = y1 + master.cellheight
            master.rect[row,column] = master.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="grid")
        
        
def loadCars(master):
    # read in the lines from the file
    #script, filename = argv                # FIX THIS LATER
    filename = "test3.txt"
    with open(filename) as f:
        content = f.readlines()
    
    # load in each car in the file
    for line in content:
        splitLine = line.split(" ")
        initCoords = splitLine[1].split(",")
        endCoords = splitLine[2].split(",")
        temp = Car(master, (int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]), splitLine[3], splitLine[4])
        master.carArray[splitLine[0]] = temp

    # check for initial collisions
    if checkAllForCollisions(master):
        print "Bad setup!"
        return
        # FIX THIS LATER TO MAKE IT ACTUALLY WORK

def drawCars(master):   #master is board
    # There are no initial collisions, so draw for real
    for index in master.carArray:
        master.carArray[index].draw(master)

    
    
class Car(object):
    # construtor
    xmin, xmax, ymin, ymax, color, direction = 0, 0, 0, 0, "", ""
    def __init__(self, master, xmin, ymin, xmax, ymax, color, direction):
        self.length = max(xmax - xmin, ymax-ymin)
        self.xmin= xmin*master.cellwidth
        self.ymin = ymin*master.cellheight
        self.xmax = xmax*master.cellwidth
        self.ymax = ymax*master.cellheight
        self.color = color
        self.direction = direction
    
    # draws a car on the board
    def draw(self, master):
        master.rect[self.xmin,self.ymin] = master.canvas.create_rectangle(self.xmin, self.ymin,self.xmax, self.ymax, fill=self.color, tags="car")
       
    # checks if two cars are colliding
    def isColliding(self, car2):
        if ((self.xmin >= car2.xmin and self.xmin < car2.xmax) and (self.ymin >= car2.ymin and self.ymin < car2.ymax)) \
            or ((self.xmax > car2.xmin and self.xmax <= car2.xmax) and (self.ymax > car2.ymin and self.ymax <= car2.ymax)):
            return True
        return False
        
    def isWin(self, master):
        if self.xmax > master.columns*master.cellwidth and self.ymin == master.winrow*master.cellheight:
            return True
        return False
        
    # moves a car somewhere else
    def move(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
           
def main():
    root = Tk()
    root.geometry('800x600+0+0')        # Make this be parameters + buffer space
    thingy = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()