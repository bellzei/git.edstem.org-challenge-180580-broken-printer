class Node:
    
    def __init__(self, color, legal_states, unsafe_states, path):
        self.color = color
        #self.parent = None
        self.children = []
        self.state = 'Not Legal'
        self.heuristic = 0
        self.depth = 0
        self.path = path + [color]

        self.check_state(legal_states, unsafe_states)
        
    def generate_children(self, legal_states, unsafe_states, path):
        children_colors = []
        color = self.color
        for i in range(len(self.color)):       # sorry this is super inefficient i think but just gonna use it for now
            child = ''
            for j in range(len(self.color)):
                if i == j:
                    if self.color[i] == '1':
                        child += '0'
                    elif self.color[i] == '0':
                        child += '1'
                else: 
                    child += self.color[j]
            children_colors.append(child)
        #print(f"node: {self.color}, childen: {children_colors}")
        #cont = input("continue? ")

        children = []
        for color in children_colors:
            child = Node(color, legal_states, unsafe_states, path)
            children.append(child)
        return children

    def calculate_heuristic(self, legal_states):
        distances = []
        for goal in legal_states:
            hammingDistance = sum(1 for bit1, bit2 in zip(self.color, goal) if bit2 != 'X' and bit1 != bit2)    # higher heuristic for more differences
            distances.append(hammingDistance)
        self.heuristic = min(distances)
    
    def check_state(self, legal_states, unsafe_states):
        if self.color in legal_states:
            self.state = 'LEGAL'

        for unsafe_state in unsafe_states:
            if all(p == 'X' or self.color[i] == p for i, p in enumerate(unsafe_state)):
                self.state = 'UNSAFE'
        


    