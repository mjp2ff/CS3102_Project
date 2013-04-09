'''
Created on Apr 1, 2013

@author: Matt and Arjun
'''

from Tkinter import *

class Example(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="red")
        self.parent = parent
        self.initUI()
    def initUI(self):
        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=1)

def main():
    root = Tk()
    w = Label(root, text="Hello, world!")
    w.pack();
    
    root.mainloop()


if __name__ == '__main__':
    main()