class Node:
    
    def __init__(self, color):
        self.color = color
        self.parent = None
        self.children = []
        self.state = 'Not Legal'
        self.heuristic = 0
        self.depth = 0
        self.path = []
        
    def generate_children(self):
        pass
        
    def calculate_heuristic(self):
        pass
    
    def check_state(self):
        pass
    