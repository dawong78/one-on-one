from django.test import TestCase
from match.models import *
from match.algorithm import *

class AlgorithmTest(TestCase):
    
    def create_person(self, name="my name", email="email@host.com"):
        p = Person.objects.create(name=name, email=email)
        p.save()
        return p
    
    def create_model(self):
        m = Model()
        numPeople = 5
        for i in range(numPeople):
            p = self.create_person("name" + str(i), "email" + str(i))
            m.add_person(p)
        return m
    
    def test_matcher(self):
        model = self.create_model()
        matcher = Matcher(model)
        results = matcher.match(0)
        print results
        
