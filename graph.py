class Graph:
    def __init__(self, directed=False):
        """
        Initialize a new Graph.
        
        :param directed: If True, creates a directed graph; otherwise, an undirected graph.
        """
        self.adj_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        
        :param vertex: The vertex to add.
        """
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, src, dest):
        """
        Add an edge between two vertices in the graph.
        
        :param src: The source vertex.
        :param dest: The destination vertex.
        """
        # Ensure both vertices exist
        if src not in self.adj_list:
            self.add_vertex(src)
        if dest not in self.adj_list:
            self.add_vertex(dest)
        
        # Add the edge from src to dest
        self.adj_list[src].append(dest)
        
        # If the graph is undirected, add an edge from dest to src as well
        if not self.directed:
            self.adj_list[dest].append(src)

    def get_neighbors(self, vertex):
        """
        Return the neighbors of a given vertex.
        
        :param vertex: The vertex whose neighbors are to be returned.
        :return: A list of adjacent vertices.
        """
        return self.adj_list.get(vertex, [])

    def __str__(self):
        """
        Return a string representation of the graph.
        """
        return '\n'.join(f'{vertex}: {neighbors}' for vertex, neighbors in self.adj_list.items())


