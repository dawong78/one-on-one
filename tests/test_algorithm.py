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
        
    def test_controller_get_group(self):
        p1 = self.create_person("name1", "email1")
        p1.save()
        p2 = self.create_person("name2", "email2")
        p2.save()
        people = [p1, p2]
        group = Group.objects.create(name="group")
        group.people = people
        group.save()
        controller = Controller()
        result = controller.get_group("group")
        self.assertEquals(result, group)
        self.assertEquals(2, len(result.people.all()))
