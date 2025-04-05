class Node:
    
    def __init__(self, color, legal_states, unsafe_states):
        self.color = color
        self.parent = None
        self.children = []
        self.state = 'Not Legal'
        self.heuristic = 0
        self.depth = 0
        self.path = []

        self.check_state(legal_states, unsafe_states)
        
    def generate_children(self, legal_states, unsafe_states):
        children_colors = []
        for i in len(self.color):
            child = self.color
            if self.color[i] == '1':
                child[i] == '0'
            elif self.color[i] == '0':
                child[i] == '1'
                

        # TODO work out children colors (flipping bits)
        
        children = []
        for color in children_colors:
            child = Node(color, legal_states, unsafe_states)

        
    def calculate_heuristic(self):
        pass
    
    def check_state(self, legal_states, unsafe_states):
        if self.color in legal_states:
            self.state = 'LEGAL'
        elif self.color in unsafe_states:
            #TODO deal with X values 
            self.state = 'UNSAFE'