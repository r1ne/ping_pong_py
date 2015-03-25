import Tkinter
import tkMessageBox
import random

"""TODO:
1)Запилить класс игровых объектов GameObject(методы - draw(), поля - x,y,width,height,bgcolor)
2)Запилить классы-потомки GameObject'a (Ball,Racket,Bonus)
3)Bitmap?
4)Больше прогить
"""
class Ball:
    def __init__(self):

    def __del__

def print_hello(event):
    tkMessageBox.showinfo("Hello","Kak cac?")

def render():
    master.after(50,render)

def draw_rectangle(event):
    w.create_rectangle(10,10,50,50, fill = "Black")

master = Tkinter.Tk()

w = Tkinter.Canvas(master, width = 800, height = 600)

w.pack()
master.bind("<Return>", print_hello)
master.bind("<Up>", draw_rectangle)

w.config(background = "#333333", borderwidth = 0)
render()
Tkinter.mainloop()
