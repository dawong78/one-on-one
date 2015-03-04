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
        