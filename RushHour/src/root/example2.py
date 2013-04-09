'''
Created on Apr 9, 2013

@author: Matt
'''
from Tkinter import *

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)
        
        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)
        
        self.blah = Button(self.hi_there, text="BLAH", command=self.say_blah)
        self.blah.pack(side=RIGHT)
        
        self.blah2 = Button(self.hi_there, text="BLAH2", command=self.say_blah)
        self.blah2.pack(side=LEFT)
        
    def say_hi(self):
        print "hi there, everyone!"
        
    def say_blah(self):
        print "I'm bored"
        
def main():
    root = Tk()
    a = App(root)   
    root.mainloop()


if __name__ == '__main__':
    main()