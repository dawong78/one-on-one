from match.models import *

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
            r = r + 1

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

    state = None
    node = None

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

    state = None

    def __init__(self, state):
        self.state = state

    def compare(self, o1, o2):
        # preference given to the highest unmatched count
        return self.state.get_unmatched_count(o2) - self.state.get_unmatched_count(o1)


class Matcher:

    model = None

    def __init__(self):
        self.__init__(Model())

    def __init__(self, model):
        self.model = model

    # Pairs up people.  If there are odd people, the odd person is matched
    # with the best pair.
    # @param offset The iteration to calculate
    # @return MatchResults
    def match(self, offset):
        return self.match(offset, None)

    # @param offset int
    # @param state State
    # @return MatchResults
    def match(self, offset, state):
        if state == None:
            state = State(self.model.get_people_count())
        matches = None
        unmatched = null
        unmatchedPair = null
        for i in range(offset+1):
            matches = match(state)
            people = self.model.people
            for match in matches:
                p1 = match.person1
                p2 = match.person2
                people.remove(p1)
                people.remove(p2)
                state.matched(self.model.index_of(p1), self.model.index_of(p2))
            if len(people) > 0:
                unmatched = people.get(0)
                unmatchedPair = findPair(state, matches, unmatched)
                state.unmatched(self.model.index_of(unmatched))
                if unmatchedPair != null:
                    state.crowded(self.model.index_of(unmatched),
                                  self.model.index_of(unmatchedPair.getPerson1()),
                                  self.model.index_of(unmatchedPair.getPerson2()))
        return MatchResults(matches, unmatched, unmatchedPair, state)

    def match(self, state):
        # create the graph that represents the relationships --
        # who can be matched with who
        g = Graph(self.model.get_people_count())
        people = self.model.people
        for p1 in range(len(people)):
            person1 = people.get(p1)
            # only need to add edges for half of graph, since graph is bidirectional
            for p2 in range(p1+1, len(people)):
                person2 = people.get(p2)
                # don't add relationships for people with exclusions
                if not self.model.is_excluded(person1, person2):
                    g.addEdge(p1, p2)
        # calc pairs
        pairs = Algorithm.find_pairs(g, state)
        matches = create_matches(pairs)
        return matches

    # Convert graph nodes to people
    # @param pairs int[][]
    # @return
    def create_matches(self, pairs):
        matches = []
        for i in range(len(pairs)):
            if pairs[i][0] >= 0 and pairs[i][1] >= 0:
                p1 = self.model.getPerson(pairs[i][0])
                p2 = self.model.getPerson(pairs[i][1])
                m = Pair(p1, p2)
                matches.append(m)
        return matches

    # Attempt to match an unmatched person to a pair.
    # First check if the pair has been crowded.
    # Second check if the pair has been matched with unmatched.
    # @param state
    # @param pairs
    # @param p
    # @return may return null if no suitable pair could be found
    def find_pair(self, state, pairs, unmatched):
        bestCrowdScore = 99999
        bestMatchScore = 99999
        bestPair = None
        ip = self.model.index_of(unmatched)
        for pair in pairs:
            p1 = pair.person1
            p2 = pair.person2
            if not self.model.is_excluded(unmatched, p1) and not self.model.is_excluded(unmatched, p2):
                ip1 = self.model.index_of(p1)
                ip2 = self.model.index_of(p2)
                # test 1: lowest crowd score
                crowdScore = state.get_crowded_count(ip1) + state.get_crowded_count(ip2)
                # test 2: lowest match score
                matchScore = state.get_matched_count(ip, ip1) + state.get_matched_count(ip, ip2)
                if bestPair == None or crowdScore < bestCrowdScore:
                    bestPair = pair
                    bestCrowdScore = crowdScore
                    bestMatchScore = matchScore
                elif crowdScore == bestCrowdScore:
                    if matchScore < bestMatchScore:
                        bestPair = pair
                        bestCrowdScore = crowdScore
                        bestMatchScore = matchScore
		return bestPair
