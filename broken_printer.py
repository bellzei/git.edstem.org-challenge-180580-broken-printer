import sys
from graph import Graph

def broken_printer(char, filename):
    # TODO
    return ''

def BFS():
    pass



def DFS(color):
    # current_node
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
