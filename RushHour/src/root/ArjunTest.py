'''
Created on Apr 5, 2013

@author: Arjun
'''
from Tkinter import *

rectanglecolor = 'orange' 
background = tk_rgb = "#%02x%02x%02x" % (100, 255, 100) 
distY = 6

root = Tk()
root.geometry('800x450+0+0') 
root.title("Rush Hour!")

# code to add widgets
can = Canvas (root,width=800,height=450,bg=background) 
can.grid()
# note that create_rectangle actually returns an integer that is used to identify 
# that shape in the context of the canvas that it was created within. 
cars = {}
cars[0] = can.create_rectangle(400,0,600,200,fill=rectanglecolor) 

# variables for moving rectangles around
x = 0
y = 0
firstTime = True

def dragMove(event):
    global firstTime
    if firstTime:
        firstTime = False
        global x, y
        x = event.x
        y = event.y
        # bbox on a rectangle returns the following tuple ((x1, y1), (x2, y2))
        tuple = can.bbox(cars[0])
    
        # array that this loop creates is x1, y1, x2, y2
        loc = {}
        for num, entry in enumerate(tuple):
            loc[num] = entry
        if x < loc[0] or x > loc[2]:
            x = 1000
        if y < loc[1] or y > loc[3]:
            y = 1000
    else:
        if x == 1000 or y == 1000:
            x = event.x
            y = event.y
            # bbox on a rectangle returns the following tuple ((x1, y1), (x2, y2))
            tuple = can.bbox(cars[0])
    
            # array that this loop creates is x1, y1, x2, y2
            loc = {}
            for num, entry in enumerate(tuple):
                loc[num] = entry
            if x < loc[0] or x > loc[2]:
                x = 1000
            if y < loc[1] or y > loc[3]:
                y = 1000
        else:
            can.move(cars[0], event.x-x, event.y-y)
            root.update()
            global x, y
            x = event.x
            y = event.y

def resetFirstTime(event):
    global firstTime
    firstTime = True

frame = Frame(root, width=800, height=450)
can.bind("<B1-Motion>", dragMove);
can.bind("<ButtonRelease-1>", resetFirstTime)

# start the game
root.mainloop()