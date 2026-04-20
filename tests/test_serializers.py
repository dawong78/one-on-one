from django.test import TestCase
from match.models import *
from match.serializers import *
from rest_framework.renderers import JSONRenderer
from datetime import datetime

class SerializersTest(TestCase):
    
    def create_group(self):
        p1 = Person.objects.create(name="name1", email="email1")
        p2 = Person.objects.create(name="name1", email="email1")
        people = [p1, p2];
        group = Group.objects.create(name="group name")
        group.people = people
        return group
        
    
    def test_render_group(self):
        group = self.create_group()
        ser = GroupSer(group)
        result = JSONRenderer().render(ser.data)
        expected = """{"id":1,"name":"group name","people":[{"id":1,"name":"name1","email":"email1"},{"id":2,"name":"name1","email":"email1"}]}"""
        self.assertEquals(expected, result)
        
    def create_result(self, group):
        result = Result.objects.create(group = group,
                date_created=datetime.now())
        people = group.people.all()
        match = Match.objects.create(result=result, person1=people[0], 
                person2=people[1])
        result.matches = [match]
        return result
        