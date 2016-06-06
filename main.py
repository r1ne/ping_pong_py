# coding=utf-8

import Tkinter
import tkFont
import tkMessageBox
import random
import math


class GameObjectManager:
    class Score:
        def __init__(self, canvas):
            self.left = 0
            self.right = 0
            self.canvas = canvas

            self.score_font = tkFont.Font(family='Droid Sans Mono', size=86)
            self.id = self.canvas.create_text(100, 100, text="SCORE", \
                    fill="#222222", font=self.score_font)
            self.change_text()

        def inc_left(self):
            self.left = self.left + 1
            self.change_text()

        def inc_right(self):
            self.right = self.right + 1
            self.change_text()

        def change_text(self):
            self.canvas.itemconfig(self.id, \
                    text="{}:{}".format(self.left, self.right))
            self.canvas.coords(self.id, self.canvas.winfo_reqwidth() / 2, \
                    self.canvas.winfo_reqheight() / 2) 

    def __init__(self, canvas, master):
        self.canvas = canvas
        self.gameObjects = []
        self.master = master
        self.score = self.Score(self.canvas)

        self.paused = 0
        self.pause_time = 60
        self.pause_afterid = 0
        gfont = font=tkFont.Font(family='Droid Sans Mono', slant="italic", size=32)
        tfont = font=tkFont.Font(family='Droid Sans Mono', slant="italic", size=16)
        left = self.canvas.winfo_reqwidth() / 2
        top = self.canvas.winfo_reqheight() / 2
        self.pauseshadow = self.canvas.create_text(left + 1, top + 1, text="timeout", \
                fill="#000000", font=gfont, state="hidden")
        self.pauseid = self.canvas.create_text(left, top, text="timeout", \
                fill="#ffffff", font=gfont, state="hidden")
        self.pausetimershadow = self.canvas.create_text(left + 1, top + 36, text="timeout", \
                fill="#000000", font=tfont, state="hidden")
        self.pausetimer = self.canvas.create_text(left, top + 35, text="timeout", \
                fill="#444444", font=tfont, state="hidden")

        master.bind("<F9>", self.pause, add="+")

        self.tick()

    def pause(self, pause_time=0):
        if (self.paused):
            self.unpause()
        else:
            if (self.pause_time > 0):
                self.paused = 1
                self.pause_timer()
                self.canvas.itemconfig(self.pauseid, state="normal")
                self.canvas.itemconfig(self.pauseshadow, state="normal")
                self.canvas.itemconfig(self.pausetimer, state="normal")
                self.canvas.itemconfig(self.pausetimershadow, state="normal")

    def pause_timer(self):
        if (self.paused):
            if (self.pause_time == 0):
                self.unpause()
                return 0

            text = "{}s left".format(self.pause_time)
            self.canvas.itemconfig(self.pausetimer, text=text)
            self.canvas.itemconfig(self.pausetimershadow, text=text)
            self.pause_time = self.pause_time - 1

            self.pause_afterid = self.master.after(1000, self.pause_timer)

    def unpause(self):
        self.paused = 0
        self.canvas.itemconfig(self.pauseid, state="hidden")
        self.canvas.itemconfig(self.pauseshadow, state="hidden")
        self.canvas.itemconfig(self.pausetimer, state="hidden")
        self.canvas.itemconfig(self.pausetimershadow, state="hidden")
        self.master.after_cancel(self.pause_afterid)

    def addRacket(self, x=0, y=0, moveupkey="w", movedownkey="s", width=20, \
            height=80, bgcolor="#ffffff"):
        r = Racket(self, x, y, moveupkey, movedownkey, width, height, bgcolor)
        self.gameObjects.append(r)

    def addObject(self, obj):
        self.gameObjects.append(obj)

    def addBall(self, x=0, y=0, angle=0, speed=7, size=20, bgcolor="#ffffff"):
        b = Ball(self, x, y, angle, speed, size, bgcolor)
        self.gameObjects.append(b)

    def tick(self):
        if not(self.paused):
            cwidth = 0
            cheight = 0
            for item in self.gameObjects:
                cwidth = self.master.winfo_reqwidth()
                #cheight = self.master.winfo_reqheight()
                if (item.type == "ball"):
                    item.move()

        self.master.after(8, self.tick)


class Ball:
    def __init__(self, gameObjectManager, x=0, y=0, angle=0,\
            speed=10, size=20, bgcolor="#ffffff"):

        self.angle = angle
        self.bgcolor = bgcolor
        self.canvas = gameObjectManager.canvas
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

                if (self.width > item.width) and (self.height > item.height):
                    s = item
                    p = self
                else:
                    s = self
                    p = item

                if (s.right() <= p.left()) or (s.left() >= p.right()):
                    if (s.delta.x > 0) and (p.delta.x > 0):
                        if (s.x > p.x):
                            p.delta.x = -p.delta.x
                        else:
                            s.delta.x = -s.delta.x
                    elif (s.delta.x < 0) and (p.delta.x < 0):
                        if (s.x > p.x):
                            s.delta.x = -s.delta.x
                        else:
                            p.delta.x = -p.delta.x
                    else:
                        s.delta.x = -s.delta.x
                        p.delta.x = -p.delta.x

                elif (s.bottom() <= p.top()) or (s.top() >= p.bottom()):
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
                elif ((self.bottom() + self.delta.y >= item.top()) or\
                     (item.timerup) and (self.bottom() + self.delta.y >= item.top() - item.speed))\
                     and (self.bottom() <= item.height / 2 + item.top()):
                        # 1.22111111 - 75 градусов в радианах
                        # 0.52333333 - 30 градусов в радианах
                        angle = -(1.22111111 - 0.52333333 * (self.x - item.x) / item.width)
                        self.delta = self.calc_projections(self.speed, angle)
                elif (self.top() + self.delta.y <= item.bottom()) or\
                     (item.timerdown) and (self.top() + self.delta.y <= item.bottom() + item.speed):
                        # 4.9716666 - 285 градусов в радианах
                        angle = -(4.9716666 + 0.52333333 * (self.x - item.x) / item.width)
                        self.delta = self.calc_projections(self.speed, angle)

        # ширина канваса
        cwidth = self.canvas.winfo_reqwidth()
        # высота канваса
        cheight = self.canvas.winfo_reqheight()

        # обрабатываем выход за поле
        # правая граница поля
        if (self.right() + self.delta.x >= cwidth):
            self.gameObjectManager.score.inc_left()
            self.canvas.coords(self.id, cwidth/2, cheight/2, cwidth/2 + self.width, cheight/2 + self.height)
            self.x = cwidth/2
            self.y = cheight/2
            return

        # левая граница поля
        if (self.left() - abs(self.delta.x) <= 0):
            self.gameObjectManager.score.inc_right()
            self.canvas.coords(self.id, cwidth/2, cheight/2, cwidth/2 + self.width, cheight/2 + self.height)
            self.x = cwidth/2
            self.y = cheight/2
            return

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
        self.speed = 10
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
        if not(self.gameObjectManager.paused):
            if (self.y > 20):
                self.y = self.y - self.speed
                self.canvas.move(self.id, 0, -self.speed)

        if (self.timerup):
            self.gameObjectManager.master.after(20, self.moveup_timer)

    def movedown_timer(self):
        if not(self.gameObjectManager.paused):
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

master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width=800, height=600, \
        highlightthickness=0, relief='ridge', background="#111111")

canvas.pack()
master.resizable(width=False, height=False)
master.title("Ping-pong")

gm = GameObjectManager(canvas, master)

gm.addBall(x=400, y=300, angle=0, speed=5, size=20)
gm.addRacket(x=20, y=canvas.winfo_reqheight() / 2 - 40)
gm.addRacket(x=canvas.winfo_reqwidth() - 40, y=canvas.winfo_reqheight() / 2 - 40, \
             moveupkey="i", movedownkey="k")

Tkinter.mainloop()
