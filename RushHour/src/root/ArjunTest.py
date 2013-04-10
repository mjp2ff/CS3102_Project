'''
Created on Apr 5, 2013

@author: Arjun
'''
from Tkinter import *
from symbol import if_stmt

rectanglecolor = 'orange' 
background = tk_rgb = "#%02x%02x%02x" % (100, 255, 100) 
distY = 6

root = Tk()
root.geometry('800x450+0+0') 
root.title("Rush Hour!")

# code to add widgets
can = Canvas (root,width=800,height=450,bg=background) 
can.grid()
# note that rect is actually just an integer that is used to identify 
# that shape in the context of the canvas that it was created within. 
rect = can.create_rectangle(400,0,600,200,fill=rectanglecolor) 

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
    else:
        can.move(rect, event.x-x, event.y-y)
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