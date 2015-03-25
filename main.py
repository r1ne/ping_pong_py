import Tkinter
import tkMessageBox
import random

class Ball()

def print_hello(event):
    tkMessageBox.showinfo("Hello","Kak cac?")

def render():
    #w.create_rectangle(random.randint(10,100),20,200,300, fill = "#000000")
    master.after(50,render)

master = Tkinter.Tk()

w = Tkinter.Canvas(master, width = 800, height = 600)

w.pack()
master.bind("<Return>", print_hello)

w.config(background = "#333333", borderwidth = 0, relief = Tkinter.GROOVE)
render()
Tkinter.mainloop()
