import sys
from node import Node

def broken_printer(char, filename):
     
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()] # Read all lines and strip any trailing newline characters
    
        if len(lines) < 3:  # Ensure the file contains at least three lines
            raise ValueError("Input file must have at least three non-empty lines.")
    
    color = lines[0]
    legal_states = [state.strip() for state in lines[1].split(',') if state.strip()]
    unsafe_states = [state.strip() for state in lines[2].split(',') if state.strip()]

    # if char == 'B':
    #     BFS(color)
    # if char == 'D':
    #     DFS(color)
    # if char == 'I':
    #     IDS(color)
    # if char == 'G':
    #     greedy(color)
    # if char == 'A':
    #     Astar(color)
    # if char == 'H':
    #     hillclimb(color)

    return

def BFS(color, legal_states, unsafe_states):
    # fringe = []
    # expanded = []
    # node = Node(color, legal_states, unsafe_states)
    # fringe.append(node)
    # if node.state == 'LEGAL':
    #     #TODO implement end case
    #     return node
    
    # elif node.state == 'UNSAFE':
    #     node = fringe[0]
    #     BFS()


    pass

def DFS(color, legal_states, unsafe_states):
    # current_node
    fringe = []
    expanded = []
    node = Node(color, legal_states, unsafe_states)
    fringe.append(node)
    node_count = 0
    while fringe != None:
        current_node = fringe.pop()
        print('current_node: ' + current_node.color)
        
        if node_count > 1000:
            print("SEARCH FAILED")
            return None, expanded
        current_node.check_state(legal_states, unsafe_states)
        # return the path and expanded nodes if the current node is LEGAL
        if current_node.state == "LEGAL":
            return current_node.path, expanded
        
        # skip to the next node in the fringe if the current node is UNSAFE
        elif current_node.state == "UNSAFE":
            continue
        
        # expanding the node only if it is not UNSAFE.
        if current_node.state != "UNSAFE":
            # adding the current_node to the 
            expanded.append(current_node)
            node_count += 1  #incrementing the count if the current node is added to the expanded list.
            # current_node.path.append(current_node.parent.path)
            # current_node.path.append()
            
            # generating all the children and appending it to the list.
            for index in range(0, len(current_node.color)):
                if current_node.color[index] == '0':
                    # child_value = current_node.color.replace(current_node.color[index], '1', 1)
                    child_value = current_node.color[:index] + '1' + current_node.color[index+1:]
                elif current_node.color[index] == '1':
                    # child_value = current_node.color.replace(current_node.color[index], '0', 1)
                    child_value = current_node.color[:index] + '0' + current_node.color[index+1:]
                # print("child value: " + child_value)
                child_node = Node(child_value, legal_states, unsafe_states)
                child_node.parent = current_node
                child_node.path.append(current_node.path)
                child_node.path.append(current_node)
                current_node.children.append(child_node)
            
            # adding the children into the fringe
            current_node.children.reverse()
            i = 0
            found = False
            for i in range (0, len(current_node.children)): 
                child = current_node.children[i]
                for node in expanded:
                    if node.color ==  child.color: 
                        found = True
                        break
                if found == False:
                    fringe.append(child)
                    print("fringe child: " +  child.color)
                i += 1
        
               

        
        
            
        
        
    
    # if node.state == 'LEGAL':
    #     #TODO implement end case
    #     return node
    
    # elif node.state == 'UNSAFE':
    #     node = fringe[0]
    # pass

def IDS(color):
    pass

def greedy(color):
    pass

def Astar(color):
    pass

def hillclimb(color):
    pass



if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     # You can modify these values to test your code
    #     char = 'D'
    #     filename = 'example1.txt'
    # else:
    #     char = sys.argv[1]
    #     filename = sys.argv[2]
    # print(broken_printer(char, filename))
    legal_states = ['111']
    unsafe_states = ['110', '101']
    path, expanded = DFS('000', legal_states, unsafe_states)
    print('path: ')
    if path != None:
        for node in path:
            print(node.color)
    # print('expanded: ', expanded)
