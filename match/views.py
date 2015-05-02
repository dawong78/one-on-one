import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

control = Controller()

# Create your views here.

def index(request):
    logger.info("index called")
    user = request.user
    logger.debug("user={}".format(user))
    if not user.is_anonymous():
        personList = Person.objects.filter(user=user)
        if len(personList) == 0:
            logger.info("new user added: {}".format(user))
            person = Person(user=user)
            person.save();
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('match/index.html',
                             context_instance=context)

@api_view(['GET'])
def current_user(request):
    user = request.user
    person = Person.objects.get(user=user)
    ser = PersonSer(person)
    return Response(ser.data)

@api_view(['GET'])
def user_groups(request):
    user = request.user
    person = Person.objects.get(user=user)
    groups = Group.objects.filter(people=person)
    ser = GroupUrlSer(groups, many="True", context={"request": request})
    return Response(ser.data)

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
    
    @detail_route(methods=["post"])
    def add_user(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Adding {} to group {}".format(person, group))
        control.add_person_to_group(person, group)
        ser = GroupUrlSer(group, context={"request": request})
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @detail_route(methods=["post"])
    def remove_user_from_group(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Removing {} from group {}".format(person, group))
        control.remove_person_from_group(person, group)
        ser = GroupUrlSer(group, context={"request": request})
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultUrlSer
    
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchUrlSer
    
