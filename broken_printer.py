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
        return DFS(color, legal_states, unsafe_states)
    if char == 'I':
        return IDS(color, legal_states, unsafe_states)
    if char == 'G':
        return greedy(color, legal_states, unsafe_states)
    if char == 'A':
        return Astar(color, legal_states, unsafe_states)
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

def DFS(color, legal_states, unsafe_states):
    fringe = []
    expanded = []
    root = Node(color, legal_states, unsafe_states, [])
    fringe.append(root)
    node_count = 0
    solution = None

    while fringe:
        current_node = fringe.pop()
        
        # Check node expansion limit
        if node_count > 1000:
            return "SEARCH FAILED" + "\n" + ",".join(n.color for n in expanded)
        
        current_node.check_state(legal_states, unsafe_states)
        
        # If current node is a goal, record solution and add it to expanded.
        if current_node.state == "LEGAL":
            solution = current_node
            expanded.append(current_node)
            break
        # If the node is UNSAFE, skip expanding it.
        elif current_node.state == "UNSAFE":
            continue
        
        # Expand the current node.
        expanded.append(current_node)
        node_count += 1
        
        # Generate children (flipping bits in ascending order)
        children = current_node.generate_children(legal_states, unsafe_states, current_node.path)
        # For DFS, push children in reverse order so that the one with the smallest index is expanded first.
        for child in reversed(children):
            # Avoid cycles: if the child’s color is already in the current path, skip it.
            if child.color not in current_node.path:
                fringe.append(child)
    
    if solution:
        # Format: first line is the path, second line is the expanded node order.
        return ",".join(solution.path) + "\n" + ",".join(n.color for n in expanded)
    else:
        return "SEARCH FAILED" + "\n" + ",".join(n.color for n in expanded)


def DFS_limited(color, legal_states, unsafe_states, depth_limit, expanded):
    """
    A depth-limited version of DFS (using your DFS style). 
    It stops expanding nodes if the depth (determined by the length of the node's path) reaches depth_limit.
    Any node with a depth equal to the limit is treated as a fringe node:
      - Its state is checked and recorded (if not UNSAFE),
      - But its children are not expanded.
    The 'expanded' list is passed by reference and updated with every node (non-UNSAFE) that is visited.
    Returns:
      - the solution node if a LEGAL state is found,
      - or "cutoff" if no solution was found within the current depth limit.
    """
    fringe = []
    # Create root node. Its constructor already sets its path as path + [color]
    root = Node(color, legal_states, unsafe_states, [])
    fringe.append(root)
    node_count = 0
    solution = None

    while fringe:
        current_node = fringe.pop()
        
        # If we've reached or exceeded the depth limit (root has depth 0, so len(path)-1 gives depth)
        if (len(current_node.path)) >= depth_limit:
            # Check the node's state and record it if it is not UNSAFE.
            current_node.check_state(legal_states, unsafe_states)
            if current_node.state != "UNSAFE":
                expanded.append(current_node)
                if current_node.state == "LEGAL":
                    solution = current_node
                    break
            # Do not expand further from this node.
            continue

        # Otherwise, process the node normally.
        current_node.check_state(legal_states, unsafe_states)
        if current_node.state == "LEGAL":
            expanded.append(current_node)
            solution = current_node
            break
        if current_node.state == "UNSAFE":
            continue
        
        expanded.append(current_node)
        node_count += 1
        
        # Generate children if within depth limit.
        children = current_node.generate_children(legal_states, unsafe_states, current_node.path)
        # For DFS, push children in reverse order so that the leftmost (first bit flip) is expanded first.
        for child in reversed(children):
            # Avoid cycles: if the child's color already appears in the current path, skip it.
            if child.color in current_node.path:
                continue
            # Update child's path.
            # child.path = current_node.path + [child.color]
            fringe.append(child)
            
    if solution:
        return solution
    else:
        return "cutoff"



def IDS(color, legal_states, unsafe_states):
    """
    Iterative Deepening Search using DFS_limited as a base.
    Repeatedly calls DFS_limited with an increasing depth limit.
    Accumulates (by reference) all nodes visited (that are not UNSAFE) in 'total_expanded'.
    Returns a string with two lines:
      - Line 1: a comma-separated path from the start state to the goal (or "SEARCH FAILED")
      - Line 2: a comma-separated list of node colors in the order they were expanded.
    """
    depth_limit = 1  # Start with a depth limit of 1 (i.e. only the root is expanded)
    total_expanded = []   # Cumulative list of nodes (instances) expanded across iterations

    while True:
        result = DFS_limited(color, legal_states, unsafe_states, depth_limit, total_expanded)
        if result != "cutoff" and result is not None:
            # Found a solution: join the path and the cumulative expanded list.
            return ",".join(result.path) + "\n" + ",".join(n.color for n in total_expanded)
        if len(total_expanded) > 1000:
            return "SEARCH FAILED" + "\n" + ",".join(n.color for n in total_expanded)
        depth_limit += 1


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

def Astar(color, legal_states, unsafe_states):

    counter = 0  # tie-breaker counter
    start_node = Node(color, legal_states, unsafe_states, [])
    start_node.calculate_heuristic(legal_states)
    # The cost (g) for the start node is 0 because len(start_node.path)-1 == 0.
    f = (len(start_node.path) - 1) + start_node.heuristic
    fringe = []
    heapq.heappush(fringe, (f, counter, start_node))
    counter += 1
    expanded = []  # to record the order in which nodes are expanded

    while fringe:
        current_f, _, node = heapq.heappop(fringe)
        
        # If the node is a goal, record it and finish.
        if node.state == 'LEGAL':
            expanded.append(node.color)
            path = node.path
            return ",".join(path) + "\n" + ",".join(expanded)
        
        # If too many nodes have been expanded, return failure.
        if len(expanded) > 1000:
            return "SEARCH FAILED" + "\n" + ",".join(expanded)
        
        # Only expand nodes that are not UNSAFE and haven't been expanded before.
        if node.state != 'UNSAFE' and node.color not in expanded:
            expanded.append(node.color)
            # Generate children (each child is produced by flipping one bit)
            children = node.generate_children(legal_states, unsafe_states, node.path)
            for child in children:
                # Avoid cycles: do not add a child if its color already appears in the path.
                if child.color in node.path:
                    continue
                # Update the child's path (child.path is already set in Node.__init__, but we ensure it)
                # child.path = node.path + [child.color]
                child.calculate_heuristic(legal_states)
                # g(n) is the cost so far: the depth of this child.
                g = len(child.path) - 1
                new_f = g + child.heuristic
                heapq.heappush(fringe, (new_f, counter, child))
                counter += 1

    # If the fringe is empty without a solution, return failure.
    return "SEARCH FAILED" + "\n" + ",".join(expanded)


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



if __name__ == '__main__':
    if len(sys.argv) < 3:
        # You can modify these values to test your code
        char = 'I'
        filename = 'example1.txt'
    else:
        char = sys.argv[1]
        filename = sys.argv[2]
    print(broken_printer(char, filename))
    # legal_states = ['111']
    # unsafe_states = ['110', '101']
    # path, expanded = DFS('000', legal_states, unsafe_states)
    # print('path: ')
    # if path != None:
    #     for node in path:
    #         print(node)
    