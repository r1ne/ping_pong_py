#  coding=cp1251

import Tkinter
import tkMessageBox
import random
import math


class GameObjectManager:
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.master = master
        self.gameObjects = []

        self.moveObjects()

    def addObject(self, obj):
        self.gameObjects.append(obj)

    def addBall(self, x=0, y=0, angle=0, speed=7, size=20, bg="#ffffff"):
        b = Ball(self, x, y, angle, speed, size, bg)
        self.gameObjects.append(b)

    def moveObjects(self):
        for item in self.gameObjects:
            item.move()

        self.master.after(25, self.moveObjects)

class Ball:
    def __init__(self, gameObjectManager, x=0, y=0, angle=0, speed=10, size=20, bg="#ffffff"):
        self.gameObjectManager = gameObjectManager
        self.speed = speed
        self.angle = angle  # в радианах
        self.delta = self.calc_projections(self.speed, self.angle)
        self.collision = False

        self.x = x
        self.y = y
        self.height = size
        self.width = size
        self.bgcolor = bg
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(self.left(), self.top(), \
                self.right(), self.bottom(), fill=self.bgcolor, \
                outline=self.bgcolor)

        self.move()

    def __del__(self):
        pass

    def left(self):
        return self.x

    def top(self):
        return self.y

    def right(self):
        return self.x + self.width

    def bottom(self):
        return self.y + self.height

    class Delta:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

    def calc_projections(self, speed, angle):
        output = self.Delta()
        output.x = speed * math.cos(angle)
        output.y = speed * math.sin(angle)

        return output

    def keypressed(self, key):
        pass

    def move(self):
        item = self.hit_detection()
        self.collision = False
        if item != 0:
            item.collision = False

            # self должен быть наименьшим из мячей
            if (self.width > item.width) and (self.height > item.height):
                s = item
                p = self
            else:
                s = self
                p = item


            if (s.right() <= p.left()) or (s.left() >= p.right()):
                # если оба мяча летят вправо, то отталкиваем левый
                if (s.delta.x > 0) and (p.delta.x > 0):
                    if (s.x > p.x):
                        p.delta.x = -p.delta.x
                    else:
                        s.delta.x = -s.delta.x
                # если оба мяча летят влево, то отталкиваем правый
                elif (s.delta.x < 0) and (p.delta.x < 0):
                    if (s.x > p.x):
                        s.delta.x = -s.delta.x
                    else:
                        p.delta.x = -p.delta.x
                else:
                    s.delta.x = -s.delta.x
                    p.delta.x = -p.delta.x

            elif (s.bottom() <= p.top()) or (s.top() >= p.bottom()):
                #если оба мяча летят вниз, то отталкиваем верхний
                if (s.delta.y > 0) and (p.delta.y > 0):
                    if (s.y > p.y):
                        p.delta.y = -p.delta.y
                    else:
                        s.delta.y = -s.delta.y
                elif (s.delta.y < 0) and (s.delta.y < 0):
                    if (s.y > p.y):
                        s.delta.y = -s.delta.y
                    else:
                        p.delta.y = -p.delta.y
                else:
                    s.delta.y = -s.delta.y
                    p.delta.y = -p.delta.y

        # ширина канваса
        cwidth = self.canvas.winfo_reqwidth()
        # высота канваса
        cheight = self.canvas.winfo_reqheight()

        # обрабатываем выход за поле
        # правая граница поля
        if (self.right() + self.delta.x >= cwidth):
            self.delta.x = -self.delta.x

        # левая граница поля
        if (self.left() - abs(self.delta.x) <= 0):
            self.delta.x = -self.delta.x

        # верхняя граница поля
        if (self.top() + self.delta.y <= 0):
            self.delta.y = -self.delta.y

        # нижняя граница поля
        if (self.bottom() + self.delta.y >= cheight):
            self.delta.y = -self.delta.y

        self.x = self.x + self.delta.x
        self.y = self.y + self.delta.y

        self.canvas.move(self.id, self.delta.x, self.delta.y)

    def hit_detection(self):
        for item in self.gameObjectManager.gameObjects:
            if (item == self) or (self.collision == True):
                continue

            if (self.right() + self.delta.x >= item.x) and \
              (self.x + self.delta.x <= item.right()) and \
              (self.bottom() + self.delta.y >= item.y) and \
              (self.y + self.delta.y <= item.bottom()):
                item.collision = True
                self.collission = True
                return item

        return 0


class Racket:
    def __init__(self, canvas):
        self.speed = 20  # скорость движения ракетки в пикселях
        self.width = 20
        self.height = 100
        self.bgcolor = "# ffffff"
        self.x = 25
        self.y = 250
        self.side = "left"
        self.canvas = canvas

    def __del__(self):
        pass

    def draw(self):
        if self.side == "left":
            self.canvas.create_rectangle(self.x, self.y, self.x + self.width, \
                    self.y + self.height, fill=self.bgcolor, outline=self.bgcolor)
        elif self.side == "right":
            if self.x < 100:
                self.x = self.canvas.winfo_reqwidth() - (self.x + self.width)
            self.canvas.create_rectangle(self.x, self.y, self.x + self.width, \
                    self.y + self.height, fill=self.bgcolor, outline=self.bgcolor)

    def keypressed(self, event):  #TODO:сделать так, чтобы можно сразу две плашки двигать
        # вдобавок это дерьмо чувствительно к раскладке
        if event.keysym == 'w' or event.char == "":
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
                    self.y += self.speed

    def keypressedDown(self, event):
        if self.y + self.height < self.canvas.winfo_reqheight() - 10:
            if (self.y + self.speed > self.canvas.winfo_reqheight() - 10):
                self.y = self.canvas.winfo_reqheight() - (10 + self.height)
            else:
                self.y += self.speed


class Bonus:
    def __init__(self, canvas):
        self.type = 0

    def __del__(self):
        pass

    def draw(self, canvas):
        pass

    def keypressed(self, key):
        pass

#  --------------------------------

# Создаем форму, в ней - канвас
master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width=800, height=600, highlightthickness=0, relief='ridge')

canvas.pack()
canvas.config(background="#111111")
master.resizable(width=False, height=False)
master.title("Ping-pong")

gm = GameObjectManager(canvas, master)
gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#b0e828")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#0ea9f1")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#f10e79")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#e7c81e")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#b0e828")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#0ea9f1")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#f10e79")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#e7c81e")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#b0e828")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#0ea9f1")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#f10e79")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#e7c81e")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#b0e828")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 15)\
        , 20, "#0ea9f1")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 16)\
        , 20, "#f10e79")

gm.addBall(random.randint(100,700), random.randint(100, 500), \
        random.uniform(0, math.pi * 2), random.randint(5, 16)\
        , 20, "#e7c81e")

Tkinter.mainloop()
