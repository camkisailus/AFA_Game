import shapes
import acf
import actions
import uuid

class SceneObject():
    def __init__(self, shape):
        self.shape = shape
        self.id = uuid.uuid4()
        self.possible_actions = [actions.Grasp()]

    def check_actions(self):
        for action in self.possible_actions:
            if action.check():
                self.possible_actions.remove(action)
                unlocked_actions = action.execute()
                for ua in unlocked_actions:
                    self.possible_actions.append(ua)
    
    def __str__(self):
        return "{}_{}".format(self.shape.name, self.id)
    
    def __eq__(self, other):
        """
            This may not work, but fingers crossed
        """
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
                
            

