import sys
from node import Node
from collections import deque
import heapq

def broken_printer(char, filename):

    with open(filename, 'r') as file:
        lines = [line.strip() for line in file] # Read all lines and strip any trailing newline characters

        if len(lines) < 3:  # Ensure the file contains at least three lines
            raise ValueError("Input file must have at least three non-empty lines.")

    color = lines[0]
    legal_states = [] if lines[1] == "" else [state.strip() for state in lines[1].split(',')]
    unsafe_states = [] if lines[2] == "" else [state.strip() for state in lines[2].split(',')]
    

    if char == 'B':
        return BFS(color, legal_states, unsafe_states)
    if char == 'D':
        return DFS(color)
    if char == 'I':
        return IDS(color)
    if char == 'G':
        return greedy(color, legal_states, unsafe_states)
    if char == 'A':
        return Astar(color)
    if char == 'H':
        return hillclimb(color, legal_states, unsafe_states)

    return

def BFS(color, legal_states, unsafe_states):
    node = Node(color, legal_states, unsafe_states, [])
    fringe = deque([node])
    expanded = []
    goal_found = False
    #print(f"legal states: {legal_states}, unsafe states: {unsafe_states}")

    while fringe:
        node = fringe.popleft()     # get the next node to expand from the fringe
        #print(node.color)
        #print(node.state)
        if node.state == 'LEGAL':
            goal_found = True
            expanded.append(node.color)
            path = node.path
            break

        elif len(expanded) > 1000:
            return "SEARCH FAILED" + "\n" + ",".join(f"{enode}" for enode in expanded)

        elif node.state != 'UNSAFE' and node.color not in expanded:   # node is valid and has not already been expanded
            expanded.append(node.color)       # add this node to the list of expanded nodes
            #print("added node to expanded, generating children now")
            children = node.generate_children(legal_states, unsafe_states, node.path)     # generating the children
            fringe.extend(children)         # adding the children to the fringe

    if goal_found:
        return ",".join(f"{pnode}" for pnode in path) + "\n" + ",".join(f"{enode}" for enode in expanded)
    else:
        return "SEARCH FAILED" + "\n" + ",".join(f"{enode}" for enode in expanded)


def DFS(color):
    # current_node
    pass

def IDS(color):
    pass

def greedy(color, legal_states, unsafe_states):
    counter = 0     # counter for tie breaking
    node = Node(color, legal_states, unsafe_states, [])
    node.calculate_heuristic(legal_states)
    fringe = []
    heapq.heappush(fringe, (node.heuristic, counter, node))
    expanded = []
    goal_found = False
    counter += 1
    #print(f"legal states: {legal_states}, unsafe states: {unsafe_states}")

    while fringe:
        h, _, node = heapq.heappop(fringe)     # get the next node to expand from the fringe
        #print(node.color)
        #print(node.state)
        if node.state == 'LEGAL':
            goal_found = True
            expanded.append(node.color)
            path = node.path
            break

        elif len(expanded) > 1000:
            print("SEARCH FAILED")
            return

        elif node.state != 'UNSAFE' and node.color not in expanded:   # node is valid and has not already been expanded
            expanded.append(node.color)       # add this node to the list of expanded nodes
            #print("added node to expanded, generating children now")
            children = node.generate_children(legal_states, unsafe_states, node.path)     # generating the children
            for child in children:
                child.calculate_heuristic(legal_states)
                heapq.heappush(fringe, (child.heuristic, counter, child))   # adding the children to the fringe in ascending order of heuristic
                counter += 1


    if goal_found:
        return ",".join(f"{pnode}" for pnode in path) + "\n" + ",".join(f"{enode}" for enode in expanded)
    else:
        return "SEARCH FAILED" + "\n" + ",".join(f"{enode}" for enode in expanded)

def Astar(color):
    pass

def hillclimb(color, legal_states, unsafe_states):
    current_node = Node(color, legal_states, unsafe_states, [])
    current_node.calculate_heuristic(legal_states)
    expanded = []
    goal_found = False

    while True:
        if current_node.state != 'UNSAFE' and current_node.color not in expanded:   # node is valid and has not already been expanded
            expanded.append(current_node.color)
            neighbours = current_node.generate_children(legal_states, unsafe_states, current_node.path)
            best_neighbour = current_node

        for neighbour in neighbours:
            if neighbour.state != "UNSAFE" and neighbour.color not in expanded:
                neighbour.calculate_heuristic(legal_states)
                if neighbour.heuristic < best_neighbour.heuristic: # compare nodes
                    best_neighbour = neighbour

        if best_neighbour == current_node:  # no change, we have reached a local optimum
            if best_neighbour.state == 'LEGAL':
                goal_found = True
                path = best_neighbour.path
            break
        
        current_node = best_neighbour

    if goal_found:
        return ",".join(f"{pnode}" for pnode in path) + "\n" + ",".join(f"{enode}" for enode in expanded)
    else:
        return "SEARCH FAILED" + "\n" + ",".join(f"{enode}" for enode in expanded)


def DFS(color):
    # current_node
    pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        char = 'B'
        filename = 'example3.txt'
    else:
        char = sys.argv[1]
        filename = sys.argv[2]
    print(broken_printer(char, filename))
