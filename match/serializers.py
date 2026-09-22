from rest_framework import serializers
from match.models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        
class PersonSer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "user", "display_name"]

class ResultSer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Result
        fields = ["id", "date_created"]

class MatchSer(serializers.ModelSerializer):
    person1 = PersonSer()
    person2 = PersonSer()
    person3 = PersonSer()
    class Meta:
        model = Match
        fields = ("id", "person1", "person2", "person3")
    
class GroupSer(serializers.ModelSerializer):
    people = serializers.PrimaryKeyRelatedField(many=True, queryset=Person.objects.all())
    latest_matches = MatchSer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ("id", "name", "owner", "people", "latest_result_date", "latest_matches")

    def create(self, validated_data):
        owner = validated_data.pop('owner', None)
        print("group create owner: ", owner)
        people = validated_data.pop('people', None)

        group = Group.objects.create(**validated_data)
        # update owner
        if owner == None:
            group.owner = None
        else:
            db_owner = Person.objects.get(id=owner.id)
            group.owner = db_owner

        # update people
        if people == None:
            group.people.set([])
        else:
            if group.people is None:
                group.people.set([])
            for person in people:
                db_person = Person.objects.get(id=person.id)
                group.people.add(db_person)

        group.save()
        return group

class PairSer(serializers.ModelSerializer):
    class Meta:
        model = Pair
        fields = ("id", "group", "person1", "person2")
    
class PersonStateSer(serializers.ModelSerializer):
    class Meta:
        model = PersonState
        fields = ("id", "group", "person", "unmatched_count", "crowd_count")
    
class PairStateSer(serializers.ModelSerializer):
    class Meta:
        model = PairState
        fields = ("id", "pair", "match_count")
    
class AddPersonGroupParamsSer(serializers.Serializer):
    person_id = serializers.IntegerField()
    def create(self, validated_data):
        return AddPersonGroupParams(**validated_data)
    def update(self, instance, validated_data):
        instance.person_id = validated_data.get("person_id", instance.person_id)
        return instance;
