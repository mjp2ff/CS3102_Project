'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
from sys import argv
import time

class Board:
    master = None
    def __init__(self, master):
        self.master = master
        master.canvas = Canvas(master, width=600, height=600, borderwidth=0, highlightthickness=0)
        master.canvas.grid(rowspan=6, columnspan=6)
        master.canvas.pack(side="top", fill="both", expand="true")
        master.rows = 6
        master.columns = 6
        master.cellwidth = (int)(master.canvas.cget('width')) / master.columns
        master.cellheight = (int)(master.canvas.cget('height')) / master.rows
        
        master.carArray = {}        # Stores all our cars that are on the board
        master.rect = {}            # Stores all the rectangles (grid).

        drawGrid(master)
        loadCars(master)
        drawCars(master)
        master.canvas.bind("<Button-1>", self.mousePressed)
        master.canvas.bind("<ButtonRelease-1>", self.mouseReleased)

    def mousePressed(self, event):
        for index in self.master.carArray:
            absoluteXMin = self.master.carArray[index].xmin*self.master.cellwidth
            absoluteXMax = self.master.carArray[index].xmax*self.master.cellwidth
            absoluteYMin = self.master.carArray[index].ymin*self.master.cellheight
            absoluteYMax = self.master.carArray[index].ymax*self.master.cellheight
            car = self.master.carArray[index]
            carDirection = self.master.carArray[index].direction
            if event.x > absoluteXMin and event.x < absoluteXMax and event.y > absoluteYMin and event.y < absoluteYMax:
                if carDirection == 'vert':
                    if event.y < (absoluteYMin + absoluteYMax) / 2:
                        print "lower vert y half"
                        car.move(0, 1)
                        if checkForCollisions(self.master):     # If that makes it collide, move it back.
                            car.move(0, -1)
                    if event.y > (absoluteYMin + absoluteYMax) / 2:
                        print "Upper vert y half"
                        car.move(0, -1)
                        if checkForCollisions(self.master):     # If that makes it collide, move it back.
                            car.move(0, 1)
                    drawGrid(self.master)
                    drawCars(self.master)
                if carDirection == 'horiz':
                    print "horiz car touched on press"
                    if event.x < (absoluteXMin + absoluteXMax) / 2:
                        print "lower horiz x half"
                        car.move(1, 0)
                        if checkForCollisions(self.master):     # If that makes it collide, move it back.
                            car.move(-1, 0)
                    if event.x > (absoluteXMin + absoluteXMax) / 2:
                        print "Upper horiz x half"
                        car.move(-1, 0)
                        if checkForCollisions(self.master):     # If that makes it collide, move it back.
                            car.move(1, 0)
                    drawGrid(self.master)
                    drawCars(self.master)
        
    def mouseReleased(self, event):      
        for index in self.master.carArray:
            absoluteXMin = self.master.carArray[index].xmin*self.master.cellwidth
            absoluteXMax = self.master.carArray[index].xmax*self.master.cellwidth
            absoluteYMin = self.master.carArray[index].ymin*self.master.cellheight
            absoluteYMax = self.master.carArray[index].ymax*self.master.cellheight
#             if event.x > absoluteXMin and event.x < absoluteXMax and event.y > absoluteYMin and event.y < absoluteYMax:
#                 print "Car touched on release!" 


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
        temp = Car((int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]), splitLine[3], splitLine[4])
        master.carArray[splitLine[0]] = temp

    # check for initial collisions
    if checkForCollisions(master):
        print "Bad setup!"
        return
        # FIX THIS LATER TO MAKE IT ACTUALLY WORK

def drawCars(master):
    # There are no initial collisions, so draw for real
    for index in master.carArray:
        master.carArray[index].draw(master)

    
    
class Car(object):
    # construtor
    xmin, xmax, ymin, ymax, color, direction = 0, 0, 0, 0, "", ""
    def __init__(self, xmin, ymin, xmax, ymax, color, direction):
        self.length = max(xmax - xmin, ymax-ymin)
        self.xmin= xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.color = color
        self.direction = direction
    
    # draws a car on the board
    def draw(self, master):
        master.rect[self.xmin,self.ymin] = master.canvas.create_rectangle(self.xmin*master.cellwidth, self.ymin*master.cellheight,self.xmax*master.cellwidth, self.ymax*master.cellheight, fill=self.color, tags="car")
       
    # checks if two cars are colliding
    def isColliding(self, car2):
        if (self.xmin >= car2.xmin and self.xmin < car2.xmax) and (self.ymin >= car2.ymin and self.ymin < car2.ymax):
            return True
        return False
        
    # moves a car somewhere else
    def move(self, dx, dy):
        if self.xmin + dx < 0 or self.ymin + dy < 0:
            print "NO!"
            return None
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy
           
def main():
    root = Tk()
    thingy = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()