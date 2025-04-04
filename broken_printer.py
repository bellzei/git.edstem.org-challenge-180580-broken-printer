import sys
from node import Node

def broken_printer(char, filename):
     
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()] # Read all lines and strip any trailing newline characters
    
        if len(lines) < 3:  # Ensure the file contains at least three lines
            raise ValueError("Input file must have at least three non-empty lines.")
    
    color = lines[0]
    legal_states = [state.strip() for state in lines[1].split(',') if state.strip()]
    illegal_states = [state.strip() for state in lines[2].split(',') if state.strip()]

    if char == 'B':
        BFS(color)
    if char == 'D':
        DFS(color)
    if char == 'I':
        IDS(color)
    if char == 'G':
        greedy(color)
    if char == 'A':
        Astar(color)
    if char == 'H':
        hillclimb(color)

    return

def BFS():

    pass

def IDS(color):
    pass

def greedy(color):
    pass

def Astar(color):
    pass

def hillclimb(color):
    pass


def DFS(color, legal_states, unsafe_states):
    fringe = []
    expanded = []
    current_node = Node(color, legal_states, unsafe_states)
    fringe.append(current_node)
    if current_node.state != "UNSAFE":
        current_node.children = current_node.generate_children()
    
    if current_node.state =="LEGAL":
        return
    elif current_node.state == "UNSAFE":
        # current_node = fringe[]
    
        
        
        
    pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        char = 'B'
        filename = 'example1.txt'
    else:
        char = sys.argv[1]
        filename = sys.argv[2]
    print(broken_printer(char, filename))
