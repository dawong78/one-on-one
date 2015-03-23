from match.models import *
from match.algorithm import *
from operator import attrgetter
import logging
import sys
import traceback
from datetime import datetime
from django.db.models import Max

log = logging.getLogger(__name__)

class Controller:
    
    def get_view_groups(self):
        """Get all the groups and their latest matches"""
        view_groups = []
        groups = Group.objects.all()
        for group in groups:
            count = Result.objects.filter(group=group).count()
            matches = []
            if count > 0:
                latest_date = Result.objects.filter(group=group)\
                        .aggregate(Max("date_created"))["date_created__max"]
                result = Result.objects.get(date_created=latest_date)
                matches = Match.objects.filter(result=result)
            view_group = ViewGroup(name=group.name, people=list(group.people.all()),
                    matches=matches)
            view_groups.append(view_group)
        return view_groups

    def add_user(self, personName, personEmail):
        """Add a new user to a group
        Create the user, if he/she does not exist

        Expected parameters:
        groupName - group to join
        personName - name of user
        personEmail - email of user
        """
        personList = Person.objects.filter(name=personName,email=personEmail)
        person = None
        if len(personList) == 0:
            # New person
            logger.debug("Creating new user: {}".format(person))
            person = Person.objects.create(name=personName,email=personEmail)
            person.save()
        
    def add_person_to_group(self, person, group):
        if group.people is None:
            group.people = []
        group.people.add(person)
        group.save()

    def create_group(self, name):
        """Create a group.
        
        Returns True if the group was added.
        False if the group already exists
        """
        groupList = Group.objects.filter(name=name)
        logger.debug("groupList={}".format(groupList))
        if len(groupList) > 0:
            log.debug("Group already exists: {}".format(name))
            return False
        else:
            logger.debug("Creating group: {}".format(name))
            group = Group.objects.create(name=name)
            group.save()
            logger.info("Created group {}".format(name))
            return True

    def run_match(self, group):
        pairStates = PairState.objects.filter(pair__group=group)
        peopleStates = PersonState.objects.filter(group=group)
        state = DbUtility.to_state(list(group.people.all()), 
                pairStates, peopleStates)
        model = DbUtility.to_model(group)
        matcher = Matcher(model)
        matchResults = matcher.match(0, state)
        results = self.save_match_results(group, matchResults)
        return results

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
                    # Create match
                    match = Match.objects.create(result=result, 
                            person1=pair.person1,
                            person2=pair.person2,
                            person3=None)
                    if pair == unmatchedPair:
                        match.person3 = unmatchedPerson
                    match.save()
                    matches.append(match)
                    
                    # Update pair state
                    self.incr_match_count(group, pair.person1,
                            pair.person2, 1)
            # Update unmatched and crowded states
            if not unmatchedPerson is None and not unmatchedPair is None:
                self.incr_unmatched_count(group, unmatchedPerson, 1)
                self.incr_crowd_count(group, unmatchedPerson, 1)
                self.incr_crowd_count(group, unmatchedPair.person1, 1)
                self.incr_crowd_count(group, unmatchedPair.person2, 1)
                self.incr_match_count(group, unmatchedPair.person1,
                        unmatchedPerson, 1)
                self.incr_match_count(group, unmatchedPair.person2,
                        unmatchedPerson, 1)
            result.matches = matches
            result.save()
            
            log.debug("finished saving match_results")
            return result
        except:
            log.debug("Error saving match results")
            traceback.print_exc(file=sys.stdout)
    
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
        
    def get_pair(self, group, person1, person2):
        # people are matched in alphabetical order in database
        if person1.name > person2.name:
            tmp = person2
            person2 = person1
            person1 = tmp
            
        pair = None
        pairList = Pair.objects.filter(person1=person1, 
                person2=person2, group = group)
        if len(pairList) == 0:
            pair = Pair.objects.create(group = group,
                    person1=person1, person2=person2)
            pair.save()
        else:
            pair = pairList[0]
        return pair

    def get_pair_state(self, group, person1, person2):
        pair = self.get_pair(group, person1, person2)
        
        pairStateList = PairState.objects.filter(pair=pair)
        pairState = None
        if len(pairStateList) > 0:
            pairState = pairStateList[0]
        else:
            pairState = PairState.objects.create(pair=pair,
                    match_count=0)
            pairState.save()
        return pairState

    def get_person_state(self, group, person):
        personStateList = PersonState.objects.filter(person=person)
        personState = None
        if len(personStateList) > 0:
            personState = personStateList[0]
        else:
            personState = PersonState.objects.create(person=person,
                    group=group, unmatched_count=0, crowd_count=0)
            personState.save()
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
        person2 - 
        """
        
        pairState = self.get_pair_state(group, person1, person2)
        # Increment state
        pairState.match_count += count
        pairState.save()
        
    def incr_unmatched_count(self, group, person, count):
        state = self.get_person_state(group, person)
        state.unmatched_count += count;
        state.save()
        
    def incr_crowd_count(self, group, person, count):
        state = self.get_person_state(group, person)
        state.crowd_count += count
        state.save()
        