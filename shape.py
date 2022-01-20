import pygame as pg



class Rectangle():
    def __init__(self, left, top, width, height, color):
        self.rect = pg.Rect(left, top, width, height)
        self.color = color

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

