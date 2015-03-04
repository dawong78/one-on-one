from django.test import TestCase
from match.models import *

class ModelsTest(TestCase):
    
    def create_person(self, name="my name", email="email@host.com"):
        return Person.objects.create(name=name, email=email)
    
    def test_create_person(self):
        p = self.create_person()
        self.assertTrue(isinstance(p, Person))
        self.assertEqual(p.name, "my name")
        self.assertEqual(p.email, "email@host.com")
        
    def test_graph(self):
        g = Graph(5)
        g.add_edge(0, 1)
        self.assertTrue(g.is_neighbor(1, 0))
        n = g.get_neighbors(0)
        self.assertEquals([1], n)
        g.remove_edge(1, 0)
        self.assertFalse(g.is_neighbor(1, 0))
        
    def test_model(self):
        p1 = self.create_person("name1", "email1")
        p2 = self.create_person("name2", "email2")
        m = Model()
        m.add_person(p1)
        m.add_person(p2)
        r = m.get_person(0)
        self.assertEquals(p1, r)
        r = m.index_of(p1)
        self.assertEquals(0, r)
        r = m.get_people_count()
        self.assertEquals(2, r)
        r = m.get_people()
        self.assertEquals([p1, p2], r)
        r = m.get_person_by_name("name1")
        self.assertEquals(p1, r)
        m.exclude(p1, p2)
        r = m.is_excluded(p1, p2)
        self.assertTrue(r)
        r = m.is_excluded(p1, p1)
        self.assertFalse(r)