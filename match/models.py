from itertools import repeat
import logging

from django.db import models
from django.contrib.auth.models import User

log = logging.getLogger(__name__)

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User)
    
    def __str__(self):
        return "username={}".format(self.user.username)

class Group(models.Model):
    name = models.CharField(max_length=255)
    people = models.ManyToManyField(Person, related_name="group.people")
    owner = models.ForeignKey(Person, related_name="group.owner", null=True)
    
    def __str__(self):
        return "name={}, owner={}, people={}".format(self.name, 
            self.owner, self.people.all())
    
    class Meta:
        ordering = ("name",)
    
class Pair(models.Model):
    group = models.ForeignKey(Group)
    person1 = models.ForeignKey(Person, related_name="pair.person1")
    person2 = models.ForeignKey(Person, related_name="pair.person2")
    def __str__(self):
        return "person1={}, person2={}".format(self.person1.user.username, 
                self.person2.user.username)
    class Meta:
        ordering = ("group__name", "person1__user__username", "person2__user__username")
    
class PersonState(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    unmatched_count = models.IntegerField()
    crowd_count = models.IntegerField()
    def __str__(self):
        return "person={}, unmatched={}, crowd={}".format(
            self.person, self.unmatched_count, self.crowd_count)
    class Meta:
        ordering = ("group", "person")
    
class PairState(models.Model):
    pair = models.ForeignKey(Pair)
    match_count = models.IntegerField()
    def __str__(self):
        return "pair={}, match_count={}".format(self.pair, self.match_count)
    class Meta:
        ordering = ("pair",)
    
class Result(models.Model):
    date_created = models.DateTimeField()
    group = models.ForeignKey(Group, related_name="results")
    class Meta:
        ordering = ("date_created",)

class Match(models.Model):
    result = models.ForeignKey(Result, related_name="matches")
    person1 = models.ForeignKey(Person, related_name="match.person1")
    person2 = models.ForeignKey(Person, related_name="match.person2")
    person3 = models.ForeignKey(Person, related_name="match.person3", null=True)
    def __str__(self):
        if (not self.person3 is None):
            return "{}, {}, {}".format(self.person1.user.username, 
                    self.person2.user.username, self.person3.user.username)
        else:
            return "%s, %s"%(self.person1.user.username, self.person2.user.username)
    class Meta:
        ordering = ("result", "person1", "person2", "person3")
    

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
            if p.user.username == name:
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

    def __init__(self, pairs=None, unmatched=None, unmatched_pair=None, 
            state=None):
        self.pairs = pairs
        self.unmatched = unmatched
        self.unmatched_pair = unmatched_pair
        self.state = state

    def __str__(self):
        return "pairs={}, unmatched={}, unmatched_pair={}, state={}"\
                .format(self.pairs, self.unmatched, self.unmatched_pair, 
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

class AddPersonGroupParams(object):
    def __init__(self, person_id=-1):
        self.person_id = person_id
        