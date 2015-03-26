# coding=cp1251

import Tkinter
import tkMessageBox
import random

"""TODO:
1)�������� ����� ������� �������� GameObject(������ - draw(), ���� - x,y,width,height,bgcolor)
2)�������� ������-������� GameObject'a (Ball,Racket,Bonus)
3)Bitmap?
4)������ �������
"""

class GameObject:
    #�������� � ����������� ������ �� ������ � ������ �������� � ����
    def __init__(self, canvas, gameObjectsList): #����������� ������
        #��������� ���� ������
        self.x = 0 #self - ��� ������ �� ������ ������ (� c# �� ���������� � ������� ����� this)
        self.y = 0
        self.width = 0
        self.height = 0
        self.bgcolor = "#bbbbbb"

        self.canvas = canvas
        self.gameObjectsList = gameObjectsList

    def __del__(self): #���������� ������
        pass #����������������� �����, ������� ������ ��� �������� ��� ������ �������

    """
    ������ ������� ��� ��������� �������
    ---
    ������ �� ����������
    bitmap - ������ �� �����, � ������� ������ ����� ��������������
    """
    def draw(self, canvas):
        pass

    """
    ������ ������� ��� �������� ������� ���� ������� �������
    ������ ������� ������ ���� ���������� ��������, ������������,
    ����� �� ������������ ������� �� ������ � ������ �����
    if (key == _Kakayatoknopka_):
        dosmth()
    else if...
    ...
    ---
    ������ �� ����������
    key - ��� ������� ������
    """
    def keypressed(self, key):
        pass


class Ball(GameObject):
    def __init__(self, canvas, gameObjectsList):
        #��������� ����� ����
        self.speed = 0
        self.angle = 0 #����� ����� � ��������
        self.deltaX = 0
        self.deltaY = 0

        #� ���������� ���� ��������
        self.x = 100
        self.y = 100
        self.height = 10
        self.width = 10
        self.bgcolor = "#ffffff"
        self.canvas = canvas #self.canvas - ���� ������, canvas - �������� ��� ������ ������������
        self.gameObjectsList = gameObjectsList

        self.move()

    def __del__(self):
        pass

    def draw(self):
        #�.�. � ������� create_rectangle ���� ���������� �� x, y, width, height, � ���������� ��������������
        x = self.x #x � self.x - ������ ����������! self.x - ���� ������, x - ���������� ������ ������
        y = self.y
        z = self.x + self.width
        p = self.y + self.height
        self.canvas.create_rectangle(x, y, z, p, fill = self.bgcolor, outline = self.bgcolor)

    def keypressed(self, key):
        pass

    def move(self):
        self.x = self.x + 10
        canvas.after(50, self.move)


class Racket(GameObject):
    def __init__(self, canvas, gameObjectsList):
        self.speed

    def __del__(self):
        pass

    def draw(self, canvas):
        pass
        #canvas.create_rectangle(width = self.width, height = self.height, fill = self.bgcolor)

    def keypressed(self, key):
        pass


class Bonus(GameObject):
    def __init__(self, canvas, gameObjectsList):
        self.type

    def __del__(self):
        pass

    def draw(self, canvas):
        pass
        #canvas.create_rectangle(width = self.width, height = self.height, fill = self.bgcolor)

    def keypressed(self, key):
        pass


#--------------------------------

def render():
    canvas.delete("all") #������� �����

    for item in gameObjectsList: #�������� ��� ���� ��������� ������ ����� ���������
        item.draw()

    master.after(50, render)


#������� �����, � ��� - ������
master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width = 800, height = 600)
canvas.pack()
canvas.config(background = "#111111", borderwidth = 0)

#������� ������� ������� � ��������� �� � ������
gameObjectsList = []
gameObjectsList.append(Ball(canvas, gameObjectsList))

#��������� ������ � ����������
render()
Tkinter.mainloop()
