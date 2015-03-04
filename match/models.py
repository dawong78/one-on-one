from django.db import models
from itertools import repeat

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    def __str__(self):
        return "name=%s, email=%s"%(self.name, self.email)
    
class Pair(models.Model):
    person1 = models.ForeignKey(Person, related_name="first_person_pair")
    person2 = models.ForeignKey(Person, related_name="second_person_pair")
    def __str__(self):
        return "person1=%s, person2=%s"%(self.person1.name, 
                self.person2.name)
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    people = models.ManyToManyField(Person)
    pairs = models.ManyToManyField(Pair)
    
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
            return "%s, %s, %s"%(self.person1.name, self.person2.name,
                    self.person3.name)
        else:
            return "%s, %s"%(self.person1.name, self.person2.name)
    

class Graph:
    size = 0
    edges = []

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

