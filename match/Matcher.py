class Matcher:

    model

    def __init__(self):
        __init__(Model())

    def __init__(self, model):
        self.model = model

    # Pairs up people.  If there are odd people, the odd person is matched
    # with the best pair.
    # @param offset The iteration to calculate
    # @return Results
    def match(self, offset):
        match(self, offset, None)

    # @param offset int
    # @param state State
    # @return Results
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
        return Results(matches, unmatched, unmatchedPair, state)

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
