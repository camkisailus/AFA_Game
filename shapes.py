import pygame as pg
import math


class Rectangle():
    def __init__(self, left, top, width, height, color):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
    
    def set_pos(self, left, top):
        self.left = left
        self.top = top

    def draw(self, win):
        pg.draw.rect(win, self.color, pg.Rect(self.left, self.top, self.width, self.height))
    
    def is_over(self, pos):
        if pos[0] > self.left and pos[0] < self.left + self.width:
            if pos[1] > self.top and pos[1] < self.top + self.height:
                return True
        return False

class Circle():
    def __init__(self, center_x, center_y, radius, color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.color = color
    
    def set_pos(self, x, y):
        self.center_x = x
        self.center_y = y
    
    def draw(self, win):
        pg.draw.circle(win, self.color, (self.center_x, self.center_y), self.radius)
    
    def is_over(self, pos):
        x1, y1 = pos[0], pos[1]
        x2, y2 = self.center_x, self.center_y
        dist = math.hypot(x1 - x2, y1 - y2)
        if dist <= self.radius:
            return True
        return False

class Spoon():
    def __init__(self, left, top):
        self.left = left
        self.top = top
        self.circle = Circle(left, top, 15, (255,0,0))
        self.x_offset = 5
        self.y_offset = self.circle.radius - 5
        self.rect = Rectangle(left-self.x_offset, top+self.y_offset, 10, 50, (255,0,0))
    
    def draw(self, win):
        self.circle.draw(win)
        self.rect.draw(win)
    
    def is_over(self, pos):
        return self.circle.is_over(pos) or self.rect.is_over(pos)
    
    def move(self, x, y):
        self.circle.center_x = x
        self.circle.center_y = y
        self.rect.left = x - self.x_offset
        self.rect.top = y + self.y_offset

class Bowl():
    def __init__(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.circle = Circle(center_x, center_y, 30, (255, 0, 0))
    
    def draw(self, win):
        self.circle.draw(win)
    
    def is_over(self, pos):
        return self.circle.is_over(pos)
    
    def move(self, x, y):
        self.circle.center_x = x
        self.circle.center_y = y
    
        




