from django.test import TestCase
from match.models import *
from match.control import Controller

class ControlTest(TestCase):
    
    def test_incr_match_count(self):
        p1 = Person.objects.create(name="name1", email="email1")
        p1.save()
        p2 = Person.objects.create(name="name2", email="email2")
        p2.save()
        people = [p1, p2]
        group = Group.objects.create(name="group")
        group.people = people
        group.save()
        controller = Controller()
        controller.incr_match_count_by_names("group", "name1", "name2", 100)
        pair = Pair.objects.get(person1=p1, person2=p2);
        pairState = PairState.objects.get(pair=pair)
        self.assertEquals(100, pairState.match_count)
