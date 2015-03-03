class Model:

    # list of Person
    people = [];

    # hash of Person -> List of Person
    exclusions = {}

    def add_person(self, person):
        self.people.append(person)

    def remove_person(self, person):
        self.people.remove(person)

    def get_person(self, i):
        return self.people.get(i)

    def index_of(self, person):
        return self.people.index(person)

    def get_people_count(self):
        return len(self.people)

    def get_people(self):
        return self.people[:]

    def get_person_by_name(self, name):
        for p in self.people:
            if p.name == name:
                return p;
        return None;

    def exclude(self, person, excludedPerson):
        excluded = self.exclusions[person]
        if excluded == None:
            excluded = []
            exclusions[person] = excluded
        excluded.append(excludedPerson)
        # bidirectional
        excluded = self.exclusions[excludedPerson]
        if excluded == None:
            excluded = []
            exclusions[excludedPerson] = excluded
        excluded.append(person)

    def is_excluded(self, person, excludedPerson):
        excluded = self.exclusions[person]
        if excluded != None:
            return excludedPerson in excluded
        return False;
