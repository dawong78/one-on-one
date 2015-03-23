import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.shortcuts import render, redirect

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

logger = logging.getLogger(__name__)
control = Controller()

# Create your views here.

def index(request):
    logger.info("index called")
    context = {}
    return render(request, "match/index.html", context)

def create_group(request):
    """Create new group"""
    name = request.POST["name"]
    error = None
    if (not control.create_group(name)):
        error = "Group name already exists"
    request.session["error_message"] = error
    return redirect("/match")
    
def create_group_matches(request):
    """Create new matches for a group"""
    group_name = request.POST["group_name"]
    logger.debug("Creating matches for group {}".format(group_name))
    match_results = control.run_match(group_name)
    logger.debug("Match results: {}".format(match_results))
    return redirect("/match")

class GroupPeopleView(APIView):
    def post(self, request, id, format=None):
        """Add a person to a group"""
        ser = AddPersonGroupParamsSer(data=request.data)
        if (ser.is_valid()):
            param = ser.save()
            person_id = param.person_id
            person = Person.objects.get(id=person_id)
            group = Group.objects.get(id=id)
            control.add_person_to_group(person, group)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PeopleViewSet(viewsets.ModelViewSet):
    """Define view behavior"""
    queryset = Person.objects.all()
    serializer_class = PersonSer
    
class GroupViewSet(viewsets.ModelViewSet):
    """Define view behavior"""
    queryset = Group.objects.all()
    serializer_class = GroupUrlSer
    
    @detail_route(methods=["post"])
    def run_match(self, request, pk=None):
        group = Group.objects.get(id=pk)
        result = control.run_match(group)
        ser = ResultUrlSer(result, context={"request": request})
        return Response(ser.data)
    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultUrlSer
    
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchUrlSer
    
