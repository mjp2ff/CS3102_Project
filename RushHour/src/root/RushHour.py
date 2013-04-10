'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
from sys import argv
import time

class Board:
    def __init__(self, master):
        master.canvas = Canvas(master, width=600, height=600, borderwidth=0, highlightthickness=0)
        master.canvas.grid(rowspan=6, columnspan=6)
        master.canvas.pack(side="top", fill="both", expand="true")
        master.rows = 6
        master.columns = 6
        master.cellwidth = (int)(master.canvas.cget('width')) / master.columns
        master.cellheight = (int)(master.canvas.cget('height')) / master.rows
        
        master.carArray = {}
        master.rect = {}
        for column in range(master.columns):
            for row in range(master.rows):
                x1 = column*master.cellwidth
                y1 = row*master.cellheight
                x2 = x1 + master.cellwidth
                y2 = y1 + master.cellheight
                master.rect[row,column] = master.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="grid")

        drawcars(master)
        
        
def drawcars(master):
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
        temp = Car((int)(initCoords[0]), (int)(initCoords[1]), (int)(endCoords[0]), (int)(endCoords[1]), splitLine[3])
        master.carArray[splitLine[0]] = temp

    # check for initial collisions
    for i in master.carArray:
        car1 = master.carArray[i]
        for j in master.carArray:
            car2 = master.carArray[j]
            if car1 != car2 and car1.isColliding(car2):
                print "Bad setup!"
                return
                # make this reject the setup later in a better way
    
    # There are no initial collisions, so draw for real
    for index in master.carArray:
        master.carArray[index].draw(master)
    
    
class Car(object):
    # construtor
    xmin, xmax, ymin, ymax, color = 0, 0, 0, 0, ""
    def __init__(self, xmin, ymin, xmax, ymax, color):
        self.length = max(xmax - xmin, ymax-ymin)
        self.xmin= xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.color = color
    
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