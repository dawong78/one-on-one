from match.models import *
from operator import attrgetter
import logging

log = logging.getLogger(__name__)

class Controller:
    
    def run_match(self, group_name):
        group = Group.objects.get(name=group_name)
        pairStates = PairState.objects.filter(pair__group=group)
        peopleStates = PersonState.objects.filter(group=group)
        state = DbUtility.to_state(list(group.people.all()), 
                pairStates, peopleStates)
        model = DbUtility.to_model(group)
        matcher = Matcher(model)
        matchResults = matcher.match(0, state)
        self.save_match_results(group, matchResults)
        return matchResults

    def get_group(self, name):
        try:
            group = Group.objects.get(name=name)
            people = group.people
            peopleStates = []
            pairStates = []
            sortedPeople = people[:]
            sortedPeople.sort(key=attrgetter("name"))
            if len(sortedPeople) > 1:
                for i in len(sortedPeople)-1:
                    person1 = sortedPeople[i]
                    for j in range(i+1, len(sortedPeople)):
                        person2 = sortedPeople[j]
                        pairStateList = PairState.objects.filter(
                            person1__name=person1.name,
                            person2__name=person2.name,
                            group = group
                        )
                        if len(pairStateList) > 0:
                            pairStates.append(pairStateList[0])
            for person in people:
                personStateList = PersonState.objects.filter(
                    person__name = person.name,
                    group = group
                )
                if len(personStateList) > 0:
                    peopleStates.append(personStateList[0])
            state = DbUtility.to_state(people, pairStates, peopleStates)
            group.state = state
            return group
        except ValueError:
            log.error(e.strerror)
            raise

    def get_group_names(self):
        results = []
        try:
            groups = Group.objects.all()
            for group in groups:
                results.append(group.name)
        except:
            log.debug("Error getting names")
        return results
	
    def save_group(self, group):
        try :
            people = group.people
            for person in people:
                person.save()
            
            for pair in group.exclusions:
                pair.save()
                
            group.save()
        except:
            log.error("Error saving group")

    def has_group(self, name):
        count = 0
        try:
            count = Group.objects.filter(name = name).count()
        except:
            log.error("Error counting group")
        return count > 0

    def save_match_results(self, group, match_results):
        try:
            log.debug("saving match_results={}".format(match_results))
            result = Result.objects.create(group=group,
                    date_created=datetime.now())
            result.save()
            matches = []
            pairs = match_results.pairs
            unmatchedPerson = match_results.unmatched
            unmatchedPair = match_results.unmatched_pair
            if not pairs is None and len(pairs) > 0:
                for pair in pairs:
                    match = Match.objects.create(result=result, 
                            person1=pair.person1,
                            person2=pair.person2,
                            person3=None)
                    if pair == unmatchedPair:
                        match.person3 = unmatchedPerson
                    match.save()
                    matches.append(match)
            result.matches = matches
            result.save()

            people = group.people
            sortedPeople = people[:]
            sortedPeople.sort(key=attrgetter("name"))
            for i in range(len(sortedPeople) - 1):
                p1 = sortedPeople[i]
                for j in range(i+1, len(sortedPeople)):
                    p2 = sortedPeople[j]
                    pairList = Pair.objects.filter(group=group, 
                            person1=p1, person2=p2)
                    pair = None
                    if len(pairList) == 0:
                        # New pair
                        pair = Pair.objects.create(group=group,
                                person1=p1, person2=p2)
                        pair.save()
                    else:
                        pair = pairList[0]
                    pairStateList = PairState.objects.filter(pair=pair)
                    pairState = None
                    if len(pairStateList) == 0:
                        pairState = PairState()
                        pairState.person1 = p1
                        pairState.person2 = p2
                        pairState.match_count = 0
                    else:
                        pairState = pairStateList[0]
                    pairState.match_count += 1
                    pairState.save()
            for i in range(len(people)):
                p = people[i]
                personState = None
                personStateList = PersonState.objects.filter(person = p)
                if len(personStateList) > 0:
                    personState = personStateList[0]
                else:
                    personState = PersonState(person=p)
                personState.unmatched_count += 1
                personState.crowd_count += 1
                personState.save()
            log.debug("finished saving match_results")
        except:
            log.debug("Error saving match results")
    
    def get_people(self):
        return People.objects.all()

    def set_crowded_count(self, person, count):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) == 0:
            personState = PersonState.objects.create(person=person)
        else:
            personState = personStateList[0]
        personState.crowd_count = count
        personState.save()

    def set_matched_count(self, p1, p2, count):
        if p1.getName() > p2.getName():
            temp = p1
            p1 = p2
            p2 = temp
        pairStateList = PairState.objects.filter(person1=p1, person2=p2)
        pairState = None
        if len(pairStateList) == 0:
            pairState = PairState.objects.create(person1=p1, person2=p2)
        else:
            pairState = pairStateList[0]
        pairState.match_count = count
        pairState.save()

    def set_unmatched_count(self, person, count):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) == 0:
            personState = PersonState.objects.create(person=person)
        else:
            personState = personStateList[0]
        personState.unmatch_count = count
        personState.save()

    def get_pair_state(self, group, person1, person2):
        # people are matched in alphabetical order in database
        if person1.name > person2.name:
            tmp = person2
            person2 = person1
            person1 = tmp
        pairStateList = PairState.objects.filter(person1=person1, 
                person2=person2, group = group)
        pairState = None
        if len(pairStateList) > 0:
            pairState = pairStateList[0]
        return pairState

    def get_person_state(self, person):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) > 0:
            personState = personStateList[0]
        return personState
    
    def incr_match_count_by_names(self, group_name, person1_name,
            person2_name, count):
        """Increment the number of times these people have been
        matched in a group.
        
        group_name - name of group
        person1_name - name of person
        perosn2_name - name of person
        """
        group = Group.objects.get(name=group_name)
        p1 = Person.objects.get(name=person1_name)
        p2 = Person.objects.get(name=person2_name)
        self.incr_match_count(group, p1, p2, count)

    def incr_match_count(self, group, person1, person2, count):
        """Increment the number of times these people have been
        matched in a group.
        
        group - 
        person1 - 
        perosn2 - 
        """
        
        # Ensure the ordering of the person
        people = [person1, person2]
        people.sort(key=attrgetter("name"))
        person1 = people[0]
        person2 = people[1]
        
        pairList = Pair.objects.filter(person1=person1, person2=person2,
                group=group)
        pair = None
        if len(pairList) == 0:
            # New pair
            pair = Pair.objects.create(person1=person1, person2=person2,
                    group = group)
            pair.save()
        else:
            pair = pairList[0]
            
        # Get the pair state
        pairStateList = PairState.objects.filter(pair=pair)
        pairState = None
        if len(pairStateList) == 0:
            # New state
            pairState = PairState.objects.create(pair=pair, match_count=0)
            pairState.save()
        else:
            pairState = pairStateList[0]
            
        # Increment state
        pairState.match_count += count
        pairState.save()