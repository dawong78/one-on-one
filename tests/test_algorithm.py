from django.test import TestCase
from match.models import *
from match.algorithm import *

class AlgorithmTest(TestCase):
    
    def create_person(self, name="my name", email="email@host.com"):
        return Person.objects.create(name=name, email=email)
    
    def create_model(self):
        m = Model()
        numPeople = 5
        for i in range(numPeople):
            m.add_person(self.create_person("name" + str(i), "email" + str(i)))
    
    def test_matcher(self):
        model = self.create_model()
        matcher = Matcher(model)
        results = matcher.match(0)
        print results
        