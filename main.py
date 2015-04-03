#  coding=cp1251

import Tkinter
import tkMessageBox
import random
import math


class GameObjectManager:
    def __init__(self, canvas, master):
        self.canvas = canvas
        self.gameObjects = []
        self.master = master

        self.moveObjects()

    def addRacket(self, x=0, y=0, moveupkey="w", movedownkey="s", width=20, \
            height=80, bgcolor="#ffffff"):
        r = Racket(self, x, y, moveupkey, movedownkey, width, height, bgcolor)
        self.gameObjects.append(r)

    def addObject(self, obj):
        self.gameObjects.append(obj)

    def addBall(self, x=0, y=0, angle=0, speed=7, size=20, bgcolor="#ffffff"):
        b = Ball(self, x, y, angle, speed, size, bgcolor)
        self.gameObjects.append(b)

    def moveObjects(self):
        for item in self.gameObjects:
            if (item.type == "ball"):
                item.move()

        self.master.after(25, self.moveObjects)

class Ball:
    def __init__(self, gameObjectManager, x=0, y=0, angle=0,\
            speed=10, size=20, bgcolor="#ffffff"):

        self.angle = angle  # в радианах
        self.bgcolor = bgcolor
        self.canvas = canvas
        self.collision = False
        self.delta = ()
        self.gameObjectManager = gameObjectManager
        self.height = size
        self.id = 0
        self.speed = speed
        self.type = "ball"
        self.width = size
        self.x = x
        self.y = y

        self.id = self.canvas.create_rectangle(self.left(), self.top(), \
                self.right(), self.bottom(), fill=self.bgcolor, \
                outline=self.bgcolor)
        self.delta = self.calc_projections(self.speed, self.angle)
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
            if (item.type == "ball"):
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
            elif (item.type == "racket"):  # если мяч self столкнулся с ракеткой item
                if (self.right() <= item.left()): # если мяч левее ракетки
                    # 2.35619449 - 135 градусов в радианах, 
                    # 1.91986218 - 110 градусов в радианах
                    angle = -(2.35619449 + 1.91986218 * (self.y - item.y) / item.height)
                    self.delta = self.calc_projections(self.speed, angle)
                elif (self.left() >= item.right()): # если мяч правее ракетки
                    # 0.785398163 - 45 градусов в радианах 
                    # 1.9198621 - 110 градусов в радианах
                    angle = -(0.785398163 - 1.91986218 * (self.y - item.y) / item.height)
                    self.delta = self.calc_projections(self.speed, angle)
                else: # FIXME: сделать нормальное отбивание мячика ракеткой сверху и снизу
                    self.delta.y = -self.delta.y

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
                self.collision = True
                return item
        return 0


class Racket:
    def __init__(self, gameObjectManager, x=0, y=0, \
            moveupkey="w", movedownkey="s", width=20, \
            height=80, bgcolor="#ffffff"):

        self.bgcolor = bgcolor
        self.canvas = gameObjectManager.canvas
        self.gameObjectManager = gameObjectManager
        self.height = height
        self.id = 0
        self.movedownkey = movedownkey
        self.moveupkey = moveupkey
        self.speed = 10  # скорость движения ракетки в пикселях
        self.timerdown = False
        self.timerup = False
        self.type = "racket"
        self.width = width
        self.x = x
        self.y = y

        self.id = canvas.create_rectangle(self.x, self.y, self.right(),\
                self.bottom(), fill=bgcolor, outline=bgcolor)

        master.bind("<KeyPress>", self.key_pressed, add="+")
        master.bind("<KeyRelease>", self.key_released, add="+")

    def __del__(self):
        pass

    def key_pressed(self, char):
        if (char.keysym == self.moveupkey):
            if (self.timerup == False):
                self.timerup = True
                self.moveup_timer()
        elif (char.keysym == self.movedownkey):
            if (self.timerdown == False):
                self.timerdown = True
                self.movedown_timer()

    def key_released(self, char):
        if (char.keysym == self.moveupkey):
            self.timerup = False
        elif (char.keysym == self.movedownkey):
            self.timerdown = False

    def moveup_timer(self):
        if (self.y > 20):
            self.y = self.y - self.speed
            self.canvas.move(self.id, 0, -self.speed)

        if (self.timerup):
            self.gameObjectManager.master.after(20, self.moveup_timer)

    def movedown_timer(self):
        if (self.bottom() < self.canvas.winfo_reqheight() - 20):
            self.y = self.y + self.speed
            self.canvas.move(self.id, 0, self.speed)

        if (self.timerdown):
            self.gameObjectManager.master.after(20, self.movedown_timer)

    def left(self):
        return self.x

    def top(self):
        return self.y

    def right(self):
        return self.x + self.width

    def bottom(self):
        return self.y + self.height


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
canvas = Tkinter.Canvas(master, width=800, height=600, \
        highlightthickness=0, relief='ridge')

canvas.pack()
canvas.config(background="#111111")
master.resizable(width=False, height=False)
master.title("Ping-pong")

gm = GameObjectManager(canvas, master)

for i in range(0, 4):
    gm.addBall(random.randint(100, 700), random.randint(100, 500), \
            random.uniform(0, math.pi * 2), random.randint(5, 15)\
            , 20, "#b0e828")

    gm.addBall(random.randint(100, 700), random.randint(100, 500), \
            random.uniform(0, math.pi * 2), random.randint(5, 15)\
            , 20, "#0ea9f1")

    gm.addBall(random.randint(100, 700), random.randint(100, 500), \
            random.uniform(0, math.pi * 2), random.randint(5, 15)\
            , 20, "#f10e79")

    gm.addBall(random.randint(100, 700), random.randint(100, 500), \
            random.uniform(0, math.pi * 2), random.randint(5, 15)\
            , 20, "#e7c81e")

gm.addRacket(20, 10)
gm.addRacket(canvas.winfo_reqwidth() - 40, 10, "i", "k")
gm.addRacket(canvas.winfo_reqwidth()/2 - 10, 300, "y", "h")

Tkinter.mainloop()
