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
    people = PersonSer(many=True, read_only=True)
    latest_matches = MatchSer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ("id", "name", "owner", "people", "latest_result_date", "latest_matches")
    
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
