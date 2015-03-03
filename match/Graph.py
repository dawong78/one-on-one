class Graph:
    size = 0
    edges = []

    def __init__(self, size):
        self.size = size
        self.edges = [size]
        for i in range(size):
            self.edges[i] = [size]

    def add_edge(n1, n2):
        if n1 == n2:
            raise Exception("Illegal assignment: x n1 == n2")
        # bidirectional
        edges[n1][n2] = 1
        edges[n2][n1] = 1

    def remove_edge(n1, n2):
        if n1 == n2:
            raise Exception("Illegal assignment: x n1 == n2")
        # bidirectional
        edges[n1][n2] = 0
        edges[n2][n1] = 0

    def is_neighbor(n1, n2):
        return (edges[n1][n2] > 0)

    def get_neighbors(n):
        a = [size]
        for i in range(size):
            if (isNeighbor(n, i)):
                a.add(i)
        return a

