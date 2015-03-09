from django.test import TestCase
from match.models import *
from match.control import Controller

class ControlTest(TestCase):
    
    def create_group(self):
        p1 = Person.objects.create(name="name1", email="email1")
        p1.save()
        p2 = Person.objects.create(name="name2", email="email2")
        p2.save()
        p3 = Person.objects.create(name="name3", email="email3")
        p3.save()
        p4 = Person.objects.create(name="name4", email="email4")
        p4.save()
        p5 = Person.objects.create(name="name5", email="email5")
        p5.save()
        people = [p1, p2, p3, p4, p5]
        group = Group.objects.create(name="group")
        group.people = people
        group.save()
        return group
    
    def print_states(self):
        print "Printing pair states:"
        states = PairState.objects.all()
        for state in states:
            print state
        print "Printing people states:"
        states = PersonState.objects.all()
        for state in states:
            print state
    
    def test_run_match(self):
        group = self.create_group()
        controller = Controller()
        for i in range(20):
            controller.run_match("group")
            self.print_states()
        
    
    def test_incr_match_count(self):
        group = self.create_group()
        controller = Controller()
        controller.incr_match_count_by_names("group", "name1", "name2", 100)
        p1 = Person.objects.get(name="name1")
        p2 = Person.objects.get(name="name2")
        pair = Pair.objects.get(person1=p1, person2=p2, group=group);
        pairState = PairState.objects.get(pair=pair)
        self.print_states()
        self.assertEquals(100, pairState.match_count)
