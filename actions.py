import shapes
import acf


class Idle():
    def __init__(self):
        self.name = "Idle"
    
    def preconditions(self, objects):
        return True
    
    def check(self, objects):
        for obj in objects:
            if not obj.shape.static:
                return False
        return True

class Grasp():
    def __init__(self):
        self.name = "Grasp"
    
    def preconditions(self, objects):
        if len(objects) > 1:
            return False
        for a in objects[0].shape.acfs:
            if isinstance(a, acf.GraspACF) and objects[0].shape.static:
                return True
        return False
    
    def check(self, scene_objs):
        if len(scene_objs) != 1:
            return False
        for so in scene_objs:
            if not so.shape.static:
                return True 
        return False
    
    def execute(self):
        """
            Action is executed, return list of next possible actions
        """
        return [Place()]

class Place():
    def __init__(self):
        self.name = "Place"
    
    def preconditions(self, objects):
        if len(objects) > 1:
            return False
        else:
            return isinstance(objects[0].shape.current_action, Grasp) 
    
    def check(self, scene_objs):
        if len(scene_objs) > 1:
            return False
        for so in scene_objs:
            if so.shape.static:
                return True
        return False

    def execute(self):
        """
            Action is executed, return list of next possible actions
        """
        return [Grasp()]

class Mix():
    def __init__(self):
        self.name = "Mix"

    def check(self, scene_objs):
        return False
    
    def preconditions(self, objects):
        if len(objects) != 2:
            return False
        for a in objects[0].shape.acfs:
            if isinstance(a, acf.StirACF):
                for other_acf in objects[1].shape.acfs:
                    if isinstance(other_acf, acf.ContainACF):
                        return True
            elif isinstance(acf, acf.ContainACF):
                for other_acf in objects[1].shape.acfs:
                    if isinstance(other_acf, acf.StirACF):
                        return True
        return False



