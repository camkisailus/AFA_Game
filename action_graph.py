import actions
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import os

class Node():
    def __init__(self, state, parent= None, children=[]):
        self.state = state
        self.children = children
        self.parent = parent
        self.id = self.state.action.name
        for obj in self.state.object_set:
            self.id += "\n"+obj.shape.name
        self.active = False

    
    def add_child(self, child):
        self.children.append(child)
    
    def has_children(self):
        return len(self.children) > 0
    
    def show(self):
        print(self)
        print("Action: {}".format(self.state.action))
        print("Object Set:")
        if self.state.object_set:
            for obj in self.state.object_set:
                print("\t{}".format(obj))
        print("Parent: {}".format(self.parent))
        print("Children")
        for child in self.children:
            if child.parent == None:
                continue
            print('\t{}'.format(child))
        print("======================")


class SceneState():
    def __init__(self, action, interacting_objects=[], other_objects=[]):
        self.action = action
        self.object_set = interacting_objects
        self.scene_objects = other_objects
    
    def check(self):
        if self.action.name == "Idle":
            return self.action.check(self.scene_objects)
        return self.action.check(self.object_set)
    
    def __eq__(self, other):
        actions_agree = (self.action == other.action)
        objects_agree = (sorted(self.object_set) == sorted(other.object_set))
        return actions_agree and objects_agree


class StateGenerator():
    def __init__(self, scene_objects=None):
        self.scene_objects = scene_objects if scene_objects else []
        self.known_actions = [actions.Grasp(), actions.Place(), actions.Mix()]
    
    def add_object(self, object):
        self.scene_objects.append(object)

    def get_combos(self, objs):
        all_combos = []
        for i in range(1,len(objs)+1):
            all_combos.append(list(combinations(objs, i)))
        all_combos = [item for sublist in all_combos for item in sublist] #flatten itertools results
        return all_combos

    
    def generate_all_states(self):
        possible_states = []
        for combo in self.get_combos(self.scene_objects):
            for action in self.known_actions:
                if action.preconditions(combo):
                    new_state = SceneState(action, combo)
                    possible_states.append(new_state)
        return possible_states

class GraphVisualizer():
    def __init__(self, nodes, save_loc, count):
        self.nodes = nodes
        self.color_map = []
        self.save_loc = save_loc
        self.G = nx.DiGraph()
        for node in self.nodes:
            self.G.add_node(node.id)
        for node in self.nodes:
            for child in node.children:
                self.G.add_edge(node.id, child.id)
        self.show(count)
    
    def show(self, count):
        self.color_map.clear()
        fname = os.path.join(self.save_loc, "full_action_graph_{}".format(count))
        for node in self.nodes:
            if node.active:
                self.color_map.append('green')
            else:
                self.color_map.append('blue')
        nx.draw_networkx(self.G, node_color=self.color_map)
        plt.show()
        #plt.savefig(fname)
        plt.clf() # clear fig
        

class ActionGraph():
    def __init__(self, scene_objects=None):
        self.scene_objects = list(scene_objects) if scene_objects else []
        self.root = Node(SceneState(action=actions.Idle(), interacting_objects=[], other_objects=self.scene_objects))
        self.root.active = True
        self.current_node = self.root
        self.sg = StateGenerator(scene_objects)
        self.undos = {"Place":"Grasp"}
        self.nodes = []
        self.save_loc = os.path.join(os.path.dirname(os.path.realpath(__file__)), "record_data")
        self.count = 0
        if not os.path.exists(self.save_loc):
            os.mkdir(self.save_loc)

    def add_object(self, object):
        self.nodes.clear()
        self.sg.add_object(object)
        self.possible_states = self.sg.generate_all_states()
        self.scene_objects.append(object)
        self.root = Node(SceneState(action=actions.Idle(), interacting_objects=[], other_objects=self.scene_objects))
        self.current_node = self.root
        self.root.active = True
        self.nodes.append(self.root)
        self.construct_graph()
    
    def construct_graph(self):
        for state in self.possible_states:
            if len(state.object_set) == 1:
                new_node = Node(state, parent=self.root, children=[self.root])
                self.root.add_child(new_node)
                self.nodes.append(new_node)
            else:
                # TODO (camkisailus): Implement logic here
                print("Skipping until we know how to find primary object in multiple object action")
        self.graph_visualizer = GraphVisualizer(self.nodes, self.save_loc, self.count)
        self.count += 1

    def check_states(self, scene_objs):
        if self.current_node.has_children():
            for child in self.current_node.children:
                # check if any of the possible next actions have happened
                if child.state.check():
                    print("State changed to {}!".format(child.state.action.name))
                    self.current_node.active = False
                    child.active = True
                    self.current_node = child
                    self.graph_visualizer.show(self.count)
                    self.count+=1
                    

    
    def update_state(self, new_state):
        try:
            if self.undos[new_state.action] == self.current_node.state.action:
                print("State Changed")
                self.current_node = self.current_node.parent
                self.current_node.show()
        except KeyError:
            for i, child in enumerate(self.current_node.children):
                if new_state == child.state:
                    print("State Changed")
                    self.current_node = child
                    self.current_node.show()
                    ## Make next level of nodes

        # for child in self.current_node.children:
        #     if state == child.state:
        #         self.current_node = child
        #         current_object_set = self.current_node.state.object_set
        #         current_scene_objects = self.current_node.state.scene_objects
        #         for object in current_object_set:
        #             for scene_object in current_scene_objects:
        #                 for action in self.known_actions:
        #                     if action.preconditions(object, scene_object):
        #                         new_scene_objects =  current_scene_objects
        #                         new_scene_objects.remove(scene_object)
        #                         new_state = Node(SceneState(action.name,[object,scene_object],new_scene_objects))
        #                         self.current_node.add_child(new_state)
        #                         self.node_list.append(new_state)
    def show(self):
        for i,node in enumerate(self.node_list):
            print("Node {}".format(i))
            node.show()
            

