# coding=cp1251

import Tkinter
import tkMessageBox
import random
import math

"""TODO:
1)�������� ����� ������� �������� GameObject(������ - draw(), ���� - x,y,width,height,bgcolor)(�������)
2)�������� ������-������� GameObject'a (Ball(�������),Racket(����� ��������),Bonus(�� ������))
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
        self.speed = random.randint(10,30)
        self.angle = random.randint(0,360) #����� ����� � ��������
        projections = self.calc_projections(self.speed, self.angle)
        self.deltaX = projections[0]
        self.deltaY = projections[1]


        #� ���������� ���� ��������
        self.x = random.randint(10,740)
        self.y = random.randint(10,540)
        self.height = 10
        self.width = self.height
        self.bgcolor = "#ffffff"
        self.canvas = canvas #self.canvas - ���� ������, canvas - �������� ��� ������ ������������
        self.gameObjectsList = gameObjectsList

        self.move()
    def __del__(self):
        pass

    def rad_to_degr(self, angle):
        return angle * 180 / math.pi

    def degr_to_rad(self, angle):
        return angle * math.pi / 180

    def calc_projections(self, speed, angle):
        output = []
        output.append(speed * math.cos(self.degr_to_rad(angle)))
        output.append(speed * math.sin(self.degr_to_rad(angle)))

        return output

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
        p = self.hit_detection()
        if p != 0:
            if (self.x + self.width >= p.x) or (self.x <= p.x + p.width):
                self.deltaX = -self.deltaX
            elif (self.y + self.height >= p.y) or (self.y <= p.y + p.height):
                self.deltaY = -self.deltaY

        if self.x <= 0 or self.x >= self.canvas.winfo_reqwidth() - self.width:    #������������ ����� �� ����
            self.deltaX = -self.deltaX
        if self.y <= 0 or self.y >= self.canvas.winfo_reqheight() - self.height:
            self.deltaY = -self.deltaY

        self.x = self.x + self.deltaX
        self.y = self.y + self.deltaY
        canvas.after(50, self.move)

    def hit_detection(self):
        for item in gameObjectsList:
            if item == self:
                continue
            if (self.x + self.width + self.deltaX >= item.x) and \
              (self.x + self.deltaX <= item.x + item.width) and \
              (self.y + self.deltaY + self.height >= item.y) and \
              (self.y + self.deltaY <= item.y + item.height):
                return item

        return 0

class Racket(GameObject):
    def __init__(self, canvas, gameObjectsList):
        self.speed = 20 #�������� �������� ������� � �������� (������/��������?)
        self.width = 20
        self.height = 100
        self.bgcolor = "#ffffff"
        self.x = 25
        self.y = 250
        self.side = "left"
        self.canvas = canvas #self.canvas - ���� ������, canvas - �������� ��� ������ ������������
        self.gameObjectsList = gameObjectsList

    def __del__(self):
        pass

    def draw(self):
        if self.side == "left":
            self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill = self.bgcolor, outline = self.bgcolor)
        elif self.side == "right":
            if self.x < 100:
                self.x = self.canvas.winfo_reqwidth() - (self.x + self.width)
            self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill = self.bgcolor, outline = self.bgcolor)

    def keypressed(self, event):    #TODO:������� ���, ����� ����� ����� ��� ������ �������
        #�������� ��� ������ ������������� � ���������
        if event.keysym == 'w' or event.char == "":#� �� ���� ��� ��������� ������� ����� � ���� � ���� ������(����� ������), ������� ���� ����� ��������� �������
            if self.y > 10 or self.y + self.height < self.canvas.winfo_reqheight() - 10:
                if self.y - self.speed < 10:
                    self.y = 10
                else:
                    self.y -= self.speed

        elif event.keysym == "s":
            if self.y + self.height < self.canvas.winfo_reqheight() - 10:
                if (self.y + self.speed > self.canvas.winfo_reqheight() - 10):
                    self.y = self.canvas.winfo_reqheight() - (10 + self.height)
                else:
                    self.y +=self.speed

    def keypressedDown(self, event):
        if self.y + self.height < self.canvas.winfo_reqheight() - 10:
            if (self.y + self.speed > self.canvas.winfo_reqheight() - 10):
                self.y = self.canvas.winfo_reqheight() - (10 + self.height)
            else:
                self.y +=self.speed


class Bonus(GameObject):
    def __init__(self, canvas, gameObjectsList):
        self.type = 0

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
canvas = Tkinter.Canvas(master, width = 800, height = 600, highlightthickness = 0, relief= 'ridge')
#canvas.update_idletasks()
canvas.pack()
canvas.config(background = "#111111")
master.resizable(width = False, height = False)
master.title("Ping-pong")

#������� ������� ������� � ��������� �� � ������
gameObjectsList = []
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))
gameObjectsList.append(Ball(canvas, gameObjectsList))

racket_left = Racket(canvas, gameObjectsList)
gameObjectsList.append(racket_left)

racket_right = Racket(canvas, gameObjectsList)
racket_right.side = "right"
gameObjectsList.append(racket_right)

"""
bb = Ball(canvas, gameObjectsList)
bb.width = 30
bb.height = 30
bb.x = 300
bb.y = 350
bb.bgcolor = "#ff0000"
gameObjectsList.append(bb)
"""
master.bind("w",racket_left.keypressed)
master.bind("s",racket_left.keypressed)
master.bind("<Up>",racket_right.keypressed)
master.bind("<Down>",racket_right.keypressedDown)
#��������� ������ � ����������
render()
#tkMessageBox.showinfo("Title", canvas.winfo_reqheight() - 10)
Tkinter.mainloop()
