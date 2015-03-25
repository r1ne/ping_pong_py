import Tkinter
import tkMessageBox
import random

#class Ball():

#def draw_rectangle(x1,y1,x2,y2):
    #w.create_rectangle(x1,y1,x2,y2, fill = "Black")

def print_hello(event):
    tkMessageBox.showinfo("Hello","Kak cac?")

def render():
    master.after(50,render)

master = Tkinter.Tk()

w = Tkinter.Canvas(master, width = 800, height = 600)

w.pack()
master.bind("<Return>", print_hello)
draw_rectangle(10,10,100,100)

w.config(background = "#333333", borderwidth = 0, relief = Tkinter.GROOVE)
render()
Tkinter.mainloop()
