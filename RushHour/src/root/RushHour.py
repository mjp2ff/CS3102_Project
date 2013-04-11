'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
import tkMessageBox
# from sys import argv
# import time

global currentCar
currentCar = None

#BLAH

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
                
        master.carArray = {}        # Stores all our cars that are on the board
        master.rect = {}            # Stores all the rectangles (grid).

        master.level = StringVar()
        master.level.set("level1.txt")
        master.menu = OptionMenu(master, master.level, "level1.txt", "level2.txt", "level3.txt", "level4.txt", \
            "level5.txt", command=self.update)
        master.menu.pack(side="right")


        self.update(None)
        master.canvas.bind("<Button-1>", self.mousePressed)
        master.canvas.bind("<Key>", self.keyPressed)

    def update(self, event):    # This is stupid I'll explain it later...
        self.clearBoard()
        self.drawGrid()
        self.loadCars()
        self.drawCars()

    def keyPressed(self, event):
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
        global currentCar
        if currentCar != None:
            if currentCar.direction == 'vert':
                if event.char == 'w':
                    currentCar.move(0, -1*self.master.cellheight)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.ymax > self.master.columns*self.master.cellheight) or (currentCar.ymin < 0):
                        currentCar.move(0, 1*self.master.cellheight)                        
                if event.char == 's':
                    currentCar.move(0, 1*self.master.cellheight)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.ymax > self.master.columns*self.master.cellheight) or (currentCar.ymin < 0):
                        currentCar.move(0, -1*self.master.cellheight)
            if currentCar.direction == 'horiz':
                if event.char == 'a':
                    currentCar.move(-1*self.master.cellwidth, 0)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.xmax > self.master.columns*self.master.cellwidth) or (currentCar.xmin < 0):
                        currentCar.move(1*self.master.cellwidth, 0)
                if event.char == 'd':
                    currentCar.move(1*self.master.cellwidth, 0)
                    if (currentCar.checkForCollisions(self.master)) or (currentCar.xmax > self.master.columns*self.master.cellwidth) or (currentCar.xmin < 0):
                        currentCar.move(-1*self.master.cellwidth, 0)
        self.clearBoard()
        self.drawGrid()
        self.drawCars()
        self.checkForWin()
      
    def mousePressed(self, event):
        global currentCar
#         print "Hi!"
        currentCar = None
        for index in self.master.carArray:
            self.master.carArray[index].tags = 'car'    # Do this to un-highlight all non-current cars
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
            if car.xmax >= self.master.columns*self.master.cellwidth and car.ymin == self.master.winrow*self.master.cellheight and car.direction == 'horiz':
                winBox = tkMessageBox.showinfo("Win Message", "Congratulations, you won!")
                self.update(None)
            
            
    def drawGrid(self):
        for column in range(self.master.columns):
            for row in range(self.master.rows):
                x1 = column*self.master.cellwidth
                y1 = row*self.master.cellheight
                x2 = x1 + self.master.cellwidth
                y2 = y1 + self.master.cellheight
                self.master.rect[row,column] = self.master.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="grid")
                if column == self.master.wincolumn and row == self.master.winrow:
                    self.master.rect[row,column+1] = self.master.canvas.create_rectangle(x2,y1,x2+(x2-x1)/10,y2, fill="orangered", tags="grid")    #Maybe change tags later?
                    # ONLY WORKS IF YOU EXIT TO THE RIGHT        

    def drawCars(self):   #master is board
        # There are no initial collisions, so draw for real
        for index in self.master.carArray:
            if self.master.carArray[index] != None:
                self.master.carArray[index].draw(self.master)

    def loadCars(self):
        # read in the lines from the file
        #script, filename = argv                # FIX THIS LATER
        with open(self.master.level.get()) as f:
            content = f.readlines()
        
        # load in each car in the file
        for line in content:
            splitLine = line.split(" ")
            initCoords = splitLine[1].split(",")
            endCoords = splitLine[2].split(",")
            temp = Car(self.master, (int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]), splitLine[3], splitLine[4], "car")
            self.master.carArray[splitLine[0]] = temp
            
    def clearBoard(self):
        self.master.canvas.delete(ALL)
    
class Car(object):
    # construtor
    xmin, xmax, ymin, ymax, color, direction, tags = 0, 0, 0, 0, "", "", ""
    def __init__(self, master, xmin, ymin, xmax, ymax, color, direction, tags):
        self.length = max(xmax - xmin, ymax-ymin)
        self.xmin= xmin*master.cellwidth
        self.ymin = ymin*master.cellheight
        self.xmax = xmax*master.cellwidth
        self.ymax = ymax*master.cellheight
        self.color = color
        self.direction = direction
        self.tags=tags
    
    # draws a car on the board
    def draw(self, master):
        if self.tags == 'current':
            master.rect[self.xmin,self.ymin] = master.canvas.create_rectangle(self.xmin+5, self.ymin+5, self.xmax-5, self.ymax-5, fill=self.color, tags=self.tags, outline = 'black', width = 5)
        else:
            master.rect[self.xmin,self.ymin] = master.canvas.create_rectangle(self.xmin+5, self.ymin+5, self.xmax-5, self.ymax-5, fill=self.color, tags=self.tags)
       
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
    root.geometry('800x600+0+0')        # Make this be parameters + buffer space
    thingy = Board(root)
    root.mainloop()

if __name__ == '__main__':
    main()