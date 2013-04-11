'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
from sys import argv
import time

global x, y, first
x = 0
y = 0
first = True

class Board:
    master = None
    def __init__(self, master):
        self.master = master
        master.canvas = Canvas(master, width=600, height=600, borderwidth=0, highlightthickness=0)
#         master.canvas.grid(rowspan=6, columnspan=6)        #Don't think I need this...
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
        master.canvas.bind("<B1-Motion>", self.mouseHeld)
        master.canvas.bind("<ButtonRelease-1>", self.mouseReleased)

    def mouseHeld(self, event):
        global x, y, first
        if first:
            first = False
            x = event.x
            y = event.y
            return
                
        for index in self.master.carArray:
            XMin = self.master.carArray[index].xmin
            XMax = self.master.carArray[index].xmax
            YMin = self.master.carArray[index].ymin
            YMax = self.master.carArray[index].ymax
#             print YMin
            car = self.master.carArray[index]
            carDirection = self.master.carArray[index].direction
            if event.x > XMin and event.x < XMax and event.y > YMin and event.y < YMax:                
                if carDirection == 'vert':
                    if not (checkForCollisions(self.master)) and not (YMax > self.master.columns*self.master.cellheight) and not (YMin < 0):
                        car.move(0, event.y-y)
                    if checkForWin(self.master):
                        print "You win!"
                if carDirection == 'horiz':
                    if not (checkForCollisions(self.master)) and not (XMax > self.master.columns*self.master.cellwidth) and not (XMin < 0):
                        car.move(event.x-x, 0)
                    if checkForWin(self.master):
                        print "You win!"
        drawGrid(self.master)
        drawCars(self.master)
                
        x = event.x
        y = event.y
        
    def mouseReleased(self, event):      
        global first
        first = True
        for index in self.master.carArray:
            XMin = self.master.carArray[index].xmin
            XMax = self.master.carArray[index].xmax
            YMin = self.master.carArray[index].ymin
            YMax = self.master.carArray[index].ymax
            car = self.master.carArray[index]
            carDirection = self.master.carArray[index].direction
            print "released!"
            if carDirection == 'vert':
                if self.master.cellheight - YMin % self.master.cellheight < YMin % self.master.cellheight:
                    car.move(0, self.master.cellheight - YMin % self.master.cellheight)
                else:
                    car.move(0, -1*(int)(YMin % self.master.cellheight))
            if carDirection == 'horiz':
                if self.master.cellwidth - XMin % self.master.cellwidth < XMin % self.master.cellwidth:
                    car.move(self.master.cellwidth - XMin % self.master.cellwidth, 0)
                else:
                    car.move(-1*(int)(XMin % self.master.cellwidth), 0)
        drawGrid(self.master)
        drawCars(self.master)

def checkForWin(master):
    for i in master.carArray:
        if master.carArray[i].isWin(master):
            return True
    return False


def checkForCollisions(master):
    for i in master.carArray:
        car1 = master.carArray[i]
        for j in master.carArray:
            car2 = master.carArray[j]
            if car1 != car2 and car1.isColliding(car2):
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
    filename = "test1.txt"
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
    if checkForCollisions(master):
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