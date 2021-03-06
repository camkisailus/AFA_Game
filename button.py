import pygame as pg

FONT = pg.font.SysFont('comicsans', 24)


class Button():
    def __init__(self, x,y, color=(0,255,0), width=100, height=20, text='', click_action='', outline=(0,0,0)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline = outline
        self.click_action = click_action
        self.text = text if text != '' else None
            
    def draw(self, win):
        pg.draw.rect(win, self.outline, (self.x-2,self.y-2,self.width+4,self.height+4), 0)
        pg.draw.rect(win, self.color, (self.x,self.y,self.width,self.height), 0)
        if self.text:
            text_rect = FONT.render(self.text, 1, (0,0,0))
            win.blit(text_rect, (self.x + (self.width/2 - text_rect.get_width()/2), self.y + (self.height/2 - text_rect.get_height()/2)))
    
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
    
    def hover(self, on):
        if on:
            self.color = (0, 0, 255)
        else:
            self.color = (0, 255, 0)
    
    def clicked(self, screen):
        pg.draw.circle(screen, (0,0,255), (250, 250), 75)
