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
def somethingClicked(event):
    global x, y
    x = event.x
    y = event.y
    print x, y
    tuple = can.bbox(rect)
    
    # array that this loop creates is x1, y1, x2, y2
    loc = {}
    for num, entry in enumerate(tuple):
        loc[num] = entry
    if x < loc[0] or x > loc[2]:
        x = 1000
    if y < loc[1] or y > loc[3]:
        y = 1000

def doneClick(event):
    if x == 1000 or y == 1000:
        print x, y
        return
    else:
        print event.x-x, event.y-y
        can.move(rect, event.x-x, event.y-y)
        root.update()
        root.after(30)

frame = Frame(root, width=800, height=450)
can.bind("<Button-1>", somethingClicked)
can.bind("<ButtonRelease-1>", doneClick)

# sample code to move a rectangle
# for i in range(100): 
#     # move the rectangle 0 in the x direction and disty in the y direction. 
#     can.move(rect, 0, distY) 
#     root.update() # update the display 
#     root.after(30) # wait 30 ms 


# start the game
root.mainloop()