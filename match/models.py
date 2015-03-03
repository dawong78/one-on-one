from django.db import models

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
    
