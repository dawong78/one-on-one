from rest_framework import serializers
from match.models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
        
class PersonSer(serializers.ModelSerializer):
    user = UserSer()
    class Meta:
        model = Person
        fields = ("id", "user")
        
class GroupSer(serializers.ModelSerializer):
    people = PersonSer(many=True)
    owner = PersonSer()
    class Meta:
        model = Group
        fields = ("id", "name", "owner", "people")
    
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
    
class ResultSer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ("id", "date_created")

class MatchSer(serializers.ModelSerializer):
    person1 = PersonSer()
    person2 = PersonSer()
    person3 = PersonSer()
    class Meta:
        model = Match
        fields = ("id", "person1", "person2", "person3")
    
class GroupUrlSer(serializers.ModelSerializer):
    people = PersonSer(many="True", read_only="True")
    owner = PersonSer(read_only="True")
    results = serializers.HyperlinkedRelatedField(many="True", read_only="True",
            view_name="result-detail")
    """Define the API representation"""
    class Meta:
        model = Group
        fields = ("id", "name", "owner", "people", "results")
        
class MatchUrlSer(serializers.ModelSerializer):
    result = serializers.HyperlinkedRelatedField(view_name="result-detail", 
            read_only="True")
    person1 = PersonSer(read_only="True")
    person2 = PersonSer(read_only="True")
    person3 = PersonSer(read_only="True")
    class Meta:
        model = Match
        fields = ("id", "result", "person1", "person2", "person3")

class ResultUrlSer(serializers.HyperlinkedModelSerializer):
    """Define the API representation"""
    group = serializers.HyperlinkedRelatedField(view_name="group-detail", 
            read_only="True")
    matches = MatchUrlSer(many="True", read_only="True")
    class Meta:
        model = Result
        fields = ("id", "group", "date_created", "matches")
        
class AddPersonGroupParamsSer(serializers.Serializer):
    person_id = serializers.IntegerField()
    def create(self, validated_data):
        return AddPersonGroupParams(**validated_data)
    def update(self, instance, validated_data):
        instance.person_id = validated_data.get("person_id", instance.person_id)
        return instance;
