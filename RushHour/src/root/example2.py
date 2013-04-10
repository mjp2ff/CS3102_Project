'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *
import time

class Board:
    def __init__(self, master):
        master.canvas = Canvas(master, width=500, height=500, borderwidth=0, highlightthickness=0)
        master.canvas.pack(side="top", fill="both", expand="true")
        master.rows = 5
        master.columns = 5
        master.cellwidth = (int)(master.canvas.cget('width')) / master.columns
        master.cellheight = (int)(master.canvas.cget('height')) / master.rows
        
        master.rect = {}
        for column in range(master.columns):
            for row in range(master.rows):
                if isprime(7*row+5*column):
                    x1 = column*master.cellwidth
                    y1 = row*master.cellheight
                    x2 = x1 + master.cellwidth
                    y2 = y1 + master.cellheight
                    master.rect[row,column] = master.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
        
        
def isprime(a):
    for x in xrange(2, int(a**0.5)+1):
        if a % x == 0:
            return False
    return True      
           
def handle_button_push():
    print "Hello there"
           
def main():
    root = Tk()
    thingy = Board(root)
    root.mainloop()


if __name__ == '__main__':
    main()