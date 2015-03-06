from django.db import models
from itertools import repeat
import logging
from operator import attrgetter

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    def __str__(self):
        return "name={}, email={}".format(self.name, self.email)
    
class Pair(models.Model):
    person1 = models.ForeignKey(Person, related_name="first_person_pair")
    person2 = models.ForeignKey(Person, related_name="second_person_pair")
    def __str__(self):
        return "person1={}, person2={}".format(self.person1.name, 
                self.person2.name)
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    people = models.ManyToManyField(Person)
    exlusions = models.ManyToManyField(Pair)
    
class PersonState(models.Model):
    person = models.ForeignKey(Person)
    unmatched_count = models.IntegerField()
    crowd_count = models.IntegerField()
    
class PairState(models.Model):
    pair = models.ForeignKey(Pair)
    match_count = models.IntegerField()
    
class Result(models.Model):
    name = models.CharField(max_length = 255)
    group = models.ForeignKey(Group)

class Match(models.Model):
    result = models.ForeignKey(Result)
    person1 = models.ForeignKey(Person, related_name="first_person_match")
    person2 = models.ForeignKey(Person, related_name="second_person_match")
    person3 = models.ForeignKey(Person, related_name="third_person_match")
    def __str__(self):
        if (person3 != None):
            return "{}, {}, {}".format(self.person1.name, self.person2.name,
                    self.person3.name)
        else:
            return "%s, %s"%(self.person1.name, self.person2.name)
    

class Graph:

    def __init__(self, size):
        self.size = size
        self.edges = []
        for i in range(size):
            self.edges.append(list(repeat(0, size)))
            
    def is_valid_node(self, n):
        if n >= self.size:
            raise Exception("Illegal node id {n}.  Size is {size}")

    def add_edge(self, n1, n2):
        self.is_valid_node(n1)
        self.is_valid_node(n2)
        if n1 == n2:
            raise Exception("Illegal assignment: x n1 == n2")
        # bidirectional
        self.edges[n1][n2] = 1
        self.edges[n2][n1] = 1

    def remove_edge(self, n1, n2):
        self.is_valid_node(n1)
        self.is_valid_node(n2)
        if n1 == n2:
            raise Exception("Illegal assignment: x n1 == n2")
        # bidirectional
        self.edges[n1][n2] = 0
        self.edges[n2][n1] = 0

    def is_neighbor(self, n1, n2):
        self.is_valid_node(n1)
        self.is_valid_node(n2)
        return (self.edges[n1][n2] > 0)

    def get_neighbors(self, n):
        self.is_valid_node(n)
        a = []
        for i in range(self.size):
            if (self.is_neighbor(n, i)):
                a.append(i)
        return a


class Model:

    def __init__(self):
        # list of Person
        self.people = []
        # hash of Person -> List of Person
        self.exclusions = {}

    def add_person(self, person):
        self.people.append(person)

    def remove_person(self, person):
        self.people.remove(person)

    def get_person(self, i):
        return self.people[i]

    def index_of(self, person):
        return self.people.index(person)

    def get_people_count(self):
        return len(self.people)

    def get_people(self):
        return self.people[:]

    def get_person_by_name(self, name):
        for p in self.people:
            if p.name == name:
                return p
        return None

    def exclude(self, person, excludedPerson):
        excluded = None
        if person in self.exclusions:
            excluded = self.exclusions[person]
        if excluded == None:
            excluded = []
            self.exclusions[person] = excluded
        excluded.append(excludedPerson)
        # bidirectional
        excluded = None
        if excludedPerson in self.exclusions:
            excluded = self.exclusions[excludedPerson]
        if excluded == None:
            excluded = []
            self.exclusions[excludedPerson] = excluded
        excluded.append(person)

    def is_excluded(self, person, excludedPerson):
        excluded = None
        if person in self.exclusions:
            excluded = self.exclusions[person]
        if excluded != None:
            return excludedPerson in excluded
        return False

class MatchResults:

    def __init__(self, pairs=None, unmatched=None, unmatchedPair=None, 
            state=None):
        self.pairs = pairs
        self.unmatched = unmatched
        self.unmatchedPair = unmatchedPair
        self.state = state

    def __str__(self):
        return "pairs={}, unmatched={}, unmatchedPair={}, state={}"\
                .format(self.pairs, self.unmatched, self.unmatchedPair, 
                self.state)
    
    
class State:

    def __init__(self, size=0):
        self.resize(size)

    def resize(self, size):
        self.size = size
        self.matched = []
        for i in range(size):
            self.matched.append(list(repeat(0, size)))
        self.unmatched = list(repeat(0, size))
        self.crowded = list(repeat(0, size))

    def add_matched(self, n1, n2):
        self.matched[n1][n2] += 1
        self.matched[n2][n1] += 1

    def set_matched(self, n1, n2, matchCount):
        self.matched[n1][n2] = matchCount
        self.matched[n2][n1] = matchCount

    def get_matched_count(self, n1, n2):
        if self.matched is None:
            return 0
        return self.matched[n1][n2]

    def clear_matches(self):
        self.matched = []
        for i in range(size):
            self.matched.append(list(repeat(0, self.size)))

    def add_unmatched(self, n):
        self.unmatched[n] += 1

    def set_unmatched(self, n, unmatchedCount):
        self.unmatched[n] = unmatchedCount

    def get_unmatched_count(self, n):
        return self.unmatched[n]

    def clear_unmatched(self):
        self.unmatched = list(repeat(0, self.size))

    def add_crowded(self, n1, n2, n3):
        self.crowded[n1] += 1
        self.crowded[n2] += 1
        self.crowded[n3] += 1

    def set_crowded(self, n, crowdCount):
        self.crowded[n] = crowdCount

    def get_crowded_count(self, n):
        return self.crowded[n]

    def clear_crowded(self):
        self.crowded = list(repeat(0, self.size))

    def __str__(self):
        tostr = "\n"
        for i in range(self.size):
            for j in range(self.size):
                tostr += str(self.matched[i][j])
                tostr += ","
            tostr += "\n"
        return tostr

class DataSource:

    log = logging.getLogger(__name__)

    def get_group(self, name):
        list = None
        try:
            list = Group.objects.get(name=name)
            people = list.people
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
                            person2__name=person2.name
                        )
                        if len(pairStateList) > 0:
                            pairStates.append(pairStateList[0])
            for person in people:
                personStateList = PersonState.objects.filter(
                    person__name = person.name
                )
                if len(personStateList) > 0:
                    peopleStates.append(personStateList[0])
            state = DbUtility.to_state(people, pairStates, peopleStates)
            list.state = state
        except Exception as e:
            DataSource.log.debug(e)
        return list

    def get_list_names(self):
        results = []
        try:
            groups = Group.objects.all()
            for group in groups:
                results.append(group.name)
        except Exception as e:
            DataSource.log.debug(null, e)
        return results
	
    def save_list(self, group):
        try :
            people = group.people
            for person in people:
                person.save()
            
            for pair in group.exclusions:
                pair.save()
                
            group.save()
        except Exception as e:
            DataSource.log.error(e)

    def has_group(self, name):
        count = 0
        try:
            count = Group.objects.filter(name = name).count()
        except Exception as e:
            DataSource.log.debug(e)
        return count > 0

    def save_results(self, group, results, name):
        try:
            DataSource.log.debug("saving results={}".format(results))
            resultList = Result.objects.filter(name = name)
            result = None
            if len(resultList) == 0:
                result = Result.objects.create(name=name, group=group)
                result.save()
            else:
                result = resultList[0]
            matches = []
            pairs = result.pairs
            unmatchedPerson = results.get_unmatched()
            unmatchedPair = results.get_unmatched_pair()
            if not pairs is None and len(pairs) > 0:
                for pair in pairs:
                    match = Match.objects.create(result=result, 
                            person1=pair.getPerson1(),
                            person2=pair.getPerson2(),
                            person3=None)
                    if pair == unmatchedPair:
                        match.person3 = unmatchedPerson
                    match.save()
                    matches.add(match)
            result.matches = matches
            result.save()

            people = group.people
            state = results.state
            sortedPeople = people[:]
            sortedPeople.sort(key=attrgetter("name"))
            for i in range(len(sortedPeople) - 1):
                p1 = sortedPeople[i]
                index1 = people.index(p1)
                for j in range(i+1, len(sortedPeople)):
                    p2 = sortedPeople[j]
                    index2 = people.index(p2)
                    newMatchCount = state.get_matched_count(index1, index2)
                    pairStateList = PairState.objects.filter(person1=p1, person2=p2)
                    if len(pairStateList) == 0:
                        pairState = PairState()
                        pairState.person1 = p1
                        pairState.person2 = p2
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
            DataSource.log.debug("finished saving results")
        except Exception as e:
            DataSource.log.debug(e)
    
    def has_results(self, name):
        count = 0
        try:
            count = Result.objects.filter(name=name).count()
        except Exception as e:
            DataSource.log.debug(e)
        return count > 0

    def get_results(self, name):
        resultList = Result.objects.filter(name = name)
        result = None
        if len(resultList) > 0:
            result = resultList[0]
        DbUtility.to_match_results(result)

    def get_result_names(self):
        names = []
        for result in Result.objects.all():
            names.append(result.name)
        return names

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

    