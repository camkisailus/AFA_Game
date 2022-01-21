import pygame as pg
pg.init()
import button
import shapes
import scene_object as SO
from itertools import permutations
import actions
import action_graph as ag
import time

TABLE_COLOR = (153, 76, 0)
SPOON_COLOR = (127, 0, 255)
BOWL_COLOR = (255, 0, 0)
CUP_COLOR = (0, 255, 255)



class Game():
    def __init__(self):
        self.win = pg.display.set_mode([800,800])
        self.actions_button = button.Button(400,50, text='Possible Actions!')
        self.buttons = [self.actions_button]
        self.shapes = []
        self.scene_objs = []
        self.dragging_shape = None
        self.possible_actions = []
        self.font = pg.font.SysFont('comicsans', 24)
        self.action_graph = ag.ActionGraph()
        

    
    def add_button(self, button):
        self.buttons.append(button)
    
    def add_scene_object(self, shape):
        so = SO.SceneObject(shape)
        self.scene_objs.append(so)
        self.action_graph.add_object(so)
        
    
    def add_shape(self, shape):
        self.shapes.append(shape)
    
    def display_actions(self):
        all_actions = ""
        for so in self.scene_objs:
            for a in so.possible_actions:
                all_actions += ','+a.name
        self.actions_button.text = all_actions

    def render(self):
        self.win.fill((255,255,255))
        for button in self.buttons:
            button.draw(self.win)
        for so in self.scene_objs:
            if so.shape == self.dragging_shape:
                continue
            so.shape.draw(self.win)
        if self.dragging_shape:
            self.dragging_shape.draw(self.win)
        pg.display.flip()
    
    
    def run(self):
        running = True
        while running:
            self.render()

            for event in pg.event.get():
                mouse_pos = pg.mouse.get_pos()
                self.action_graph.check_states(self.scene_objs)
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_over(mouse_pos):
                            if button.click_action == 'add_spoon':
                                spoon = shapes.Spoon(10, 10, SPOON_COLOR)
                                self.add_scene_object(spoon)
                            elif button.click_action == 'add_bowl':
                                bowl = shapes.Bowl(10, 10, BOWL_COLOR)
                                self.add_scene_object(bowl)
                    for so in self.scene_objs:
                        if so.shape.is_over(mouse_pos):
                            if self.dragging_shape:
                                # new_state = ag.SceneState(actions.Place().name, [so])
                                # self.action_graph.update_state(new_state)
                                self.dragging_shape = None
                                so.shape.static = True
                            else:
                                # new_state = ag.SceneState(actions.Grasp().name, [so])
                                # self.action_graph.update_state(new_state)
                                self.dragging_shape = so.shape
                                so.shape.static = False
                
                if event.type == pg.MOUSEMOTION:
                    for button in self.buttons:
                        if button.is_over(mouse_pos):
                            button.hover(True)
                        else:
                            button.hover(False)
                    if self.dragging_shape:
                        self.dragging_shape.move(mouse_pos[0], mouse_pos[1])



                    
                    
            

def main():
    game = Game()
    spoon_button = button.Button(400, 10, text='Spoons!', click_action='add_spoon')
    game.add_button(spoon_button)
    bowl_button = button.Button(400, 30, text='Bowls!', click_action='add_bowl')
    game.add_button(bowl_button)
    game.run()



if __name__ == '__main__':
    main()
