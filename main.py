import Tkinter
import tkMessageBox
import random

#class Ball():

def print_hello(event):
    tkMessageBox.showinfo("Hello","Kak cac?")

def render():
    master.after(50,render)

master = Tkinter.Tk()

w = Tkinter.Canvas(master, width = 800, height = 600)

w.pack()
master.bind("<Return>", print_hello)
master.bind("<Return>", w.create_rectangle(10,10,50,50, fill = "Black"))

print_hello

w.config(background = "#333333", borderwidth = 0)
render()
Tkinter.mainloop()
