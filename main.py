# coding=cp1251

import Tkinter
import tkMessageBox
import random

"""TODO:
1)Запилить класс игровых объектов GameObject(методы - draw(), поля - x,y,width,height,bgcolor)
2)Запилить классы-потомки GameObject'a (Ball,Racket,Bonus)
3)Bitmap?
4)Больше прогить
"""

class GameObject:
    #передаем в конструктор ссылку на канвас и список объектов в игре
    def __init__(self, canvas, gameObjectsList): #конструктор класса
        #объявляем поля класса
        self.x = 0 #self - это ссылка на объект класса (в c# мы обращались к объекту через this)
        self.y = 0
        self.width = 0
        self.height = 0
        self.bgcolor = "#bbbbbb"

        self.canvas = canvas
        self.gameObjectsList = gameObjectsList

    def __del__(self): #деструктор класса
        pass #зарезервированное слово, которое служит как заглушка для пустых методов

    """
    шаблон функции для отрисовки объекта
    ---
    ничего не возвращает
    bitmap - ссылка на буфер, в котором объект будет отрисовываться
    """
    def draw(self, canvas):
        pass

    """
    шаблон функции для передачи объекту кода нажатой клавиши
    внутри функции должен быть реализован механизм, определяющий,
    нужно ли обрабатывать нажатие на кнопку с данным кодом
    if (key == _Kakayatoknopka_):
        dosmth()
    else if...
    ...
    ---
    ничего не возвращает
    key - код нажатой кнопки
    """
    def keypressed(self, key):
        pass


class Ball(GameObject):
    def __init__(self, canvas, gameObjectsList):
        #объявляем новые поля
        self.speed = 0
        self.angle = 0 #пусть будет в радианах
        self.deltaX = 0
        self.deltaY = 0

        #и определяем поля родителя
        self.x = 100
        self.y = 100
        self.height = 10
        self.width = 10
        self.bgcolor = "#ffffff"
        self.canvas = canvas #self.canvas - поле класса, canvas - аргумент при вызове конструктора
        self.gameObjectsList = gameObjectsList

        self.move()

    def __del__(self):
        pass

    def draw(self):
        #т.к. в функцию create_rectangle надо передавать не x, y, width, height, а координаты прямоугольника
        x = self.x #x и self.x - разные переменные! self.x - поле класса, x - переменная внутри метода
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
    canvas.delete("all") #очищаем экран

    for item in gameObjectsList: #вызываем для всех элементов списка метод отрисовки
        item.draw()

    master.after(50, render)


#Создаем форму, в ней - канвас
master = Tkinter.Tk()
canvas = Tkinter.Canvas(master, width = 800, height = 600)
canvas.pack()
canvas.config(background = "#111111", borderwidth = 0)

#Создаем игровые объекты и добавляем их в список
gameObjectsList = []
gameObjectsList.append(Ball(canvas, gameObjectsList))

#запускаем таймер с отрисовкой
render()
Tkinter.mainloop()
