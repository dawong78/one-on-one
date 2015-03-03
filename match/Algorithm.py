class Algorithm:
    
    @staticmethod
    def find_path(g):
        path = []

        # randomize start nodes
        size = g.getSize()
        roots = [size]
        for i in range(size):
            roots[i] = i
        roots = shuffle(roots)
        success = False
        r = 0
        while not success and r < len(roots):
            success = findPath(g, roots[r], path)

        return path

    @staticmethod
    def shuffle(a):
        b = a[:]
        max_index = len(a) - 1
        for i in range(len(a)):
            c = random.randint(0, max_index)
            # swap
            tmp = b[i]
            b[i] = b[c]
            b[c] = tmp
        return b

    @staticmethod
    def find_path(g, root, path):
        path.append(root)
        if len(path) == g.size:
            return True
        neighbors = g.get_neighbors(root)
        success = False
        for neighbor in neighbors:
            if not neighbor in path:
                success = find_path(g, neighbor, path)
                if success:
                    break
        if not success:
            path.remove(root)
        return success

    @staticmethod
    def find_pairs(g, state):
        # init nodes
        size = g.size
        nodes = []
        for i in len(size):
            nodes.append(i)
        # sort the nodes so that the ones that have been unmatched
        # are matched first
        cmp = NodeWeightComparator(state)
        nodes.sort(cmp.compare)
        pairs = findPairs(g, state, nodes)
        return pairs

    @staticmethod
    def find_pairs(g, state, nodes):
        usedNodes = []
        numPairs = math.floor(g.size / 2)
        pairs = []
        for i in range(numPairs):
            pair.append([2])
        for i in range(numPairs):
            for j in range(len(pairs[i])):
                pairs[i][j] = -1
        pairCount = 0
        count = 0
        while pairCount < numPairs and count < (numPairs * 2):
            # get the next unmatched node
            node = -1
            for n in nodes:
                if not n in usedNodes:
                    node = n
                    break
            # find the others that the node may be matched with
            neighbors = g.get_neighbors(node)
            # sort the neighbors so that neighbors who haven't been matched
            # with this node get higher priority.  Secondly, neighbors who
            # have been unmatched the most get higher priority.
            cmp = NeighborComparator(state, node)
            neighbors.sort(cmp.compare)
            for i in range(len(neighbors)):
                n = neighbors.get(i)
                if not n in usedNodes:
                    # found a match
                    pairs[pairCount][0] = node
                    pairs[pairCount][1] = n
                    usedNodes.append(node)
                    usedNodes.append(n)
                    pairCount = pairCount + 1
                    break
            count = count + 1
        return pairs

    class NeighborComparator:

        state
        node

        def __init__(self, state, node):
            self.state = state
            self.node = node

        def compare(self, o1, o2):
            # preference given to the smallest match count
            c = self.state.get_matched_count(self.node, o1) - self.state.get_matched_count(node, o2)
            if c == 0:
                # preference given to the highest unmatched count
                c = self.state.get_unmatched_count(o2) - self.state.get_unmatched_count(o1)
            return c

    class NodeWeightComparator:

        state

        def __init__(self, state):
            self.state = state

        def compare(self, o1, o2):
            # preference given to the highest unmatched count
            return self.state.get_unmatched_count(o2) - self.state.get_unmatched_count(o1)

