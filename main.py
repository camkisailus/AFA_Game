import pygame as pg
import button
import shapes
pg.init()

class Game():
    def __init__(self):
        self.win = pg.display.set_mode([800,800])
        self.buttons = []
        self.shapes = []
        self.dragging_shape = None
    
    def add_button(self, button):
        self.buttons.append(button)
    
    def add_shape(self, shape):
        self.shapes.append(shape)


    def render(self):
        self.win.fill((255,255,255))
        for button in self.buttons:
            button.draw(self.win)
        for shape in self.shapes:
            shape.draw(self.win)
        pg.display.flip()
    
    
    def run(self):
        running = True
        while running:
            self.render()
            for event in pg.event.get():
                mouse_pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_over(mouse_pos):
                            if button.click_action == 'add_spoon':
                                spoon = shapes.Spoon(10, 10)
                                self.add_shape(spoon)
                            elif button.click_action == 'add_bowl':
                                bowl = shapes.Bowl(10, 10)
                                self.add_shape(bowl)
                    for shape in self.shapes:
                        if shape.is_over(mouse_pos):
                            if self.dragging_shape:
                                self.dragging_shape = None
                            else:
                                self.dragging_shape = shape
                
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons:
                        if button.is_over(mouse_pos):
                            button.hover(True)
                        else:
                            button.hover(False)
                    if self.dragging_shape:
                        self.dragging_shape.move(mouse_pos[0], mouse_pos[1])
                        #self.dragging_shape.set_pos(mouse_pos[0]-self.dragging_shape.width/2, mouse_pos[1]-self.dragging_shape.height/2)


                    
                    
            

def main():
    game = Game()
    spoon_button = button.Button(400, 10, text='Spoons!', click_action='add_spoon')
    game.add_button(spoon_button)
    bowl_button = button.Button(400, 30, text='Bowls!', click_action='add_bowl')
    game.add_button(bowl_button)
    game.run()



if __name__ == '__main__':
    main()


