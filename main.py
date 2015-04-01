#  coding=cp1251

import Tkinter
import tkMessageBox
import random
import math


class GameObjectManager:
    """docstring for GameObjectManager"""
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.master = master
        self.gameObjects = []

    def addObject(self, obj):
        self.gameObjects.append(obj)

    def addBall(self, x=0, y=0, angle=0, speed=5, size=20, bg="#ffffff"):
        b = Ball(self.canvas, x, y, angle, speed, size, bg)
        self.gameObjects.append(b)


class Ball:
    def __init__(self, canvas, x=0, y=0, angle=0, speed=10, size=20, bg="#ffffff"):
        # объявляем новые поля
        self.speed = speed
        self.angle = angle  # в радианах
        self.delta = self.calc_projections(self.speed, self.angle)

        # и определяем поля родителя
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
        #p = self.hit_detection()
        #if p != 0:
            #if (self.x + self.width >= p.x) or (self.x <= p.x + p.width):
                #self.deltaX = -self.deltaX
            #elif (self.y + self.height >= p.y) or (self.y <= p.y + p.height):
                #self.deltaY = -self.deltaY

        # обрабатываем выход за поле
        if (self.x <= 0) or (self.right() >= self.canvas.winfo_reqwidth()):
            self.delta.x = -self.delta.x

        if (self.y <= 0) or (self.bottom() >= self.canvas.winfo_reqheight()):
            self.delta.y = -self.delta.y
        #if self.x - abs(self.delta.x) <= 0:
            #self.x = self.x - self.delta.x
            #self.delta.x = -self.delta.x

        #if abs(self.canvas.winfo_reqwidth() - self.right() <= self.delta.x):
            #self.x = self.canvas.winfo_reqwidth() - \
                    #(-self.canvas.winfo_reqwidth() + self.delta.x + self.right())
            #self.delta.x = -self.delta.x

        #if self.y - abs(self.delta.y) <= 0:
            #self.y = self.y - self.delta.y
            #self.delta.y = -self.delta.y

        #if abs(self.canvas.winfo_reqheight() - self.bottom() <= self.delta.y):
            #self.y = self.canvas.winfo_reqheight() - \
                    #(-self.canvas.winfo_reqheight() + self.delta.y + self.bottom())
            #self.delta.y = -self.delta.y

        self.x = self.x + self.delta.x
        self.y = self.y + self.delta.y

        self.canvas.move(self.id, self.delta.x, self.delta.y)
        canvas.after(50, self.move)

    #def hit_detection(self):
        #for item in gameObjectsList:
            #if item == self:
                #continue
            #if (self.x + self.width + self.deltaX >= item.x) and \
              #(self.x + self.deltaX <= item.x + item.width) and \
              #(self.y + self.deltaY + self.height >= item.y) and \
              #(self.y + self.deltaY <= item.y + item.height):
                #return item

        #return 0


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
# canvas.update_idletasks()
canvas.pack()
canvas.config(background="#111111")
master.resizable(width=False, height=False)
master.title("Ping-pong")

gm = GameObjectManager(canvas, master)
gm.addBall(10, 20, random.uniform(0, math.pi * 2), random.randint(10, 30), 20, "#ff0000")
gm.addBall(10, 20, random.uniform(0, math.pi * 2), random.randint(10, 30), 20, "red")
gm.addBall(10, 20, random.uniform(0, math.pi * 2), random.randint(10, 30), 20, "red")
gm.addBall(10, 20, random.uniform(0, math.pi * 2), random.randint(10, 30), 20, "red")

Tkinter.mainloop()
