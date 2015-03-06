from match.models import *
import math
from itertools import repeat
from operator import attrgetter
import logging

log = logging.getLogger(__name__)

class Algorithm:
    
    @staticmethod
    def find_path(g):
        path = []

        # randomize start nodes
        size = g.size
        roots = []
        for i in range(size):
            roots.append(i)
        roots = Algorithm.shuffle(roots)
        success = False
        r = 0
        while not success and r < len(roots):
            success = Algorithm.findPath(g, roots[r], path)
            r += 1

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
                success = Algorithm.find_path(g, neighbor, path)
                if success:
                    break
        if not success:
            path.remove(root)
        return success

    @staticmethod
    def get_graph_nodes(g, state):
        # init nodes
        size = g.size
        nodes = []
        for i in range(size):
            nodes.append(i)
        # sort the nodes so that the ones that have been unmatched
        # are matched first
        nodes.sort(key=lambda node: state.get_unmatched_count(node))
        return nodes

    @staticmethod
    def find_pairs(g, state, nodes=None):
        if nodes is None:
            nodes = Algorithm.get_graph_nodes(g, state)
        usedNodes = []
        numPairs = int(math.floor(g.size / 2))
        pairs = []
        for i in range(numPairs):
            pairs.append(list(repeat(-1, 2)))
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
                n = neighbors[i]
                if not n in usedNodes:
                    # found a match
                    pairs[pairCount][0] = node
                    pairs[pairCount][1] = n
                    usedNodes.append(node)
                    usedNodes.append(n)
                    pairCount += 1
                    break
            count += 1
        return pairs

class NeighborComparator:

    def __init__(self, state=None, node=None):
        self.state = state
        self.node = node

    def compare(self, o1, o2):
        # preference given to the smallest match count
        c = self.state.get_matched_count(self.node, o1) - self.state.get_matched_count(self.node, o2)
        if c == 0:
            # preference given to the highest unmatched count
            c = self.state.get_unmatched_count(o2) - self.state.get_unmatched_count(o1)
        return c

class Matcher:

    def __init__(self, model=None):
        self.model = model

    # Pairs up people.  If there are odd people, the odd person is matched
    # with the best pair.
    #
    # @param offset int
    # @param state State
    # @return MatchResults
    def match(self, offset, state=None):
        if state == None:
            state = State(self.model.get_people_count())
        matches = None
        unmatched = None
        unmatchedPair = None
        for i in range(offset+1):
            matches = self.match_people(state)
            people = self.model.people[:]
            for match in matches:
                p1 = match.person1
                p2 = match.person2
                people.remove(p1)
                people.remove(p2)
                state.add_matched(self.model.index_of(p1), self.model.index_of(p2))
            if len(people) > 0:
                unmatched = people[0]
                unmatchedPair = self.find_pair(state, matches, unmatched)
                state.add_unmatched(self.model.index_of(unmatched))
                if not unmatchedPair is None:
                    state.add_crowded(self.model.index_of(unmatched),
                            self.model.index_of(unmatchedPair.person1),
                            self.model.index_of(unmatchedPair.person2))
        return MatchResults(matches, unmatched, unmatchedPair, state)

    def match_people(self, state):
        # create the graph that represents the relationships --
        # who can be matched with who
        g = Graph(self.model.get_people_count())
        people = self.model.people
        for p1 in range(len(people)):
            person1 = people[p1]
            # only need to add edges for half of graph, since graph is bidirectional
            for p2 in range(p1+1, len(people)):
                person2 = people[p2]
                # don't add relationships for people with exclusions
                if not self.model.is_excluded(person1, person2):
                    g.add_edge(p1, p2)
        # calc pairs
        pairs = Algorithm.find_pairs(g, state)
        matches = self.create_matches(pairs)
        return matches

    # Convert graph nodes to people
    # @param pairs int[][]
    # @return
    def create_matches(self, pairs):
        matches = []
        for i in range(len(pairs)):
            if pairs[i][0] >= 0 and pairs[i][1] >= 0:
                p1 = self.model.get_person(pairs[i][0])
                p2 = self.model.get_person(pairs[i][1])
                m = Pair(person1=p1, person2=p2)
                matches.append(m)
        return matches

    # Attempt to match an unmatched person to a pair.
    # First check if the pair has been crowded.
    # Second check if the pair has been matched with unmatched.
    # @param state
    # @param pairs
    # @param p
    # @return may return None if no suitable pair could be found
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


class DbUtility:
    
    @staticmethod
    def to_model(group):
        model = Model()
        model.people = list(group.people.all())
        return model

    @staticmethod
    def to_state(people, pairStates, peopleStates):
        state = State(len(people))
        for pairState in pairStates:
            index1 = people.index(pairState.getPerson1())
            index2 = people.index(pairState.getPerson2())
            state.set_matched(index1, index2, pairState.match_count)
        for personState in peopleStates:
                index = people.index(personState.person)
                state.set_unmatched(index, personState.unmatched_count)
                state.set_crowded(index, personState.crowd_count)
        return state

    @staticmethod
    def to_states(people, state):
        pairStates = []
        peopleStates = []
        for i in len(people)-1:
            p1 = people[i]
            for j in range(i+1, len(people)):
                p2 = people[j]
                pairState = PairState();
                pairState.person1 = p1
                pairState.person2 = p2
                pairState.set_match_count(state.get_matched_count(i, j))
                pairStates.append(pairState)
        for i in range(len(people)):
            p = people[i]
            personState = PersonState()
            personState.person = p
            personState.set_uunmatch_count(state.get_unmatched_count(i))
            personState.set_crowd_count(state.get_crowded_count(i))
            peopleStates.append(personState)
        return (pairStates, peopleStates)
    
    @staticmethod
    def to_match_results(result):
        """Convert Result from database to MatchResult"""
        results = MatchResults()
        if not result is None:
            matches = []
            unmatchedPair = None
            unmatchedPerson = None
            dbMatches = result.matches
            if not dbMatches is None:
                for dbMatch in dbMatches:
                    p1 = dbMatch.person1
                    p2 = dbMatch.person2
                    p3 = dbMatch.person3
                    pair = Pair(person1=p1, person2=p2)
                    matches.append(pair)
                    if not p3 is None:
                        unmatchedPair = pair
                        unmatchedPerson = p3
            results.pairs = matches
            results.unmatched_pair = unmatchedPair
            results.unmatched = unmatchedPerson
        return results

class Controller:
    
    def run_match(self, group_name):
        group = Group.objects.get(name=group_name)
        pairStates = PairState.objects.filter(pair__group=group)
        peopleStates = PersonState.objects.filter(group=group)
        state = DbUtility.to_state(list(group.people.all()), 
                pairStates, peopleStates)
        model = DbUtility.to_model(group)
        matcher = Matcher(model)
        matchResults = matcher.match(0, state)
        self.save_match_results(group, matchResults)
        return matchResults

    def get_group(self, name):
        group = None
        try:
            group = Group.objects.get(name=name)
            people = group.people
            peopleStates = []
            airStates = []
            sortedPeople = people[:]
            sortedPeople.sort(key=attrgetter("name"))
            if len(sortedPeople) > 1:
                for i in len(sortedPeople)-1:
                    person1 = sortedPeople[i]
                    for j in range(i+1, len(sortedPeople)):
                        person2 = sortedPeople[j]
                        pairStateList = PairState.objects.filter(
                            person1__name=person1.name,
                            person2__name=person2.name,
                            group = group
                        )
                        if len(pairStateList) > 0:
                            pairStates.append(pairStateList[0])
            for person in people:
                personStateList = PersonState.objects.filter(
                    person__name = person.name,
                    group = group
                )
                if len(personStateList) > 0:
                    peopleStates.append(personStateList[0])
            state = DbUtility.to_state(people, pairStates, peopleStates)
            group.state = state
        except Exception as e:
            log.debug(e)
        return group

    def get_group_names(self):
        results = []
        try:
            groups = Group.objects.all()
            for group in groups:
                results.append(group.name)
        except Exception as e:
            log.debug(null, e)
        return results
	
    def save_group(self, group):
        try :
            people = group.people
            for person in people:
                person.save()
            
            for pair in group.exclusions:
                pair.save()
                
            group.save()
        except Exception as e:
            log.error(e)

    def has_group(self, name):
        count = 0
        try:
            count = Group.objects.filter(name = name).count()
        except Exception as e:
            log.debug(e)
        return count > 0

    def save_match_results(self, group, match_results):
        try:
            log.debug("saving match_results={}".format(match_results))
            result = Result.objects.create(group=group)
            result.save()
            matches = []
            pairs = match_results.pairs
            unmatchedPerson = match_results.unmatched
            unmatchedPair = match_results.unmatched_pair
            if not pairs is None and len(pairs) > 0:
                for pair in pairs:
                    match = Match.objects.create(result=result, 
                            person1=pair.person1,
                            person2=pair.person2,
                            person3=None)
                    if pair == unmatchedPair:
                        match.person3 = unmatchedPerson
                    match.save()
                    matches.append(match)
            result.matches = matches
            result.save()

            people = group.people
            state = match_results.state
            sortedPeople = people[:]
            sortedPeople.sort(key=attrgetter("name"))
            for i in range(len(sortedPeople) - 1):
                p1 = sortedPeople[i]
                index1 = people.index(p1)
                for j in range(i+1, len(sortedPeople)):
                    p2 = sortedPeople[j]
                    index2 = people.index(p2)
                    newMatchCount = state.get_matched_count(index1, index2)
                    pairList = Pair.objects.filter(group=group, 
                            person1=p1, person2=p2)
                    pair = None
                    if len(pairList) == 0:
                        # New pair
                        pair = Pair.objects.create(group=group,
                                person1=p1, person2=p2)
                        pair.save()
                    else:
                        pair = pairList[0]
                    pairStateList = PairState.objects.filter(pair=pair)
                    pairState = None
                    if len(pairStateList) == 0:
                        pairState = PairState()
                        pairState.person1 = p1
                        pairState.person2 = p2
                    else:
                        pairState = pairStateList[0]
                    pairState.match_count += 1
                    pairState.save()
            for i in range(len(people)):
                p = people[i]
                personState = None
                personStateList = PersonState.objects.filter(person = p)
                if len(personStateList) > 0:
                    personState = personStateList[0]
                else:
                    personState = PersonState(person=p)
                personState.unmatched_count += 1
                personState.crowd_count += 1
                personState.save()
            log.debug("finished saving match_results")
        except Exception as e:
            log.debug(e)
    
    def get_People(self):
        return People.objects.all()

    def set_crowded_count(self, person, count):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) == 0:
            personState = PersonState.objects.create(person=person)
        else:
            personState = personStateList[0]
        personState.crowd_count = count
        personState.save()

    def set_matched_count(self, p1, p2, count):
        if p1.getName() > p2.getName():
            temp = p1
            p1 = p2
            p2 = temp
        pairStateList = PairState.objects.filter(person1=p1, person2=p2)
        pairState = None
        if len(pairStateList) == 0:
            pairState = PairState.objects.create(person1=p1, person2=p2)
        else:
            pairState = pairStateList[0]
        pairState.match_count = count
        pairState.save()

    def set_unmatched_count(self, person, count):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) == 0:
            personState = PersonState.objects.create(person=person)
        else:
            personState = personStateList[0]
        personState.unmatch_count = count
        personState.save()

    def get_pair_state(self, person1, person2):
        # people are matched in alphabetical order in database
        if person1.getName() > person2.getName():
            tmp = person2
            person2 = person1
            person1 = tmp
        pairStateList = PairState.objects.filter(person1=person1, 
                person2=person2)
        pairState = None
        if len(pairStateList) > 0:
            pairState = pairStateList[0]
        return pairState

    def get_person_state(self, person):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) > 0:
            personState = personStateList[0]
        return personState

    