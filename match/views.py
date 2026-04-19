import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.context import RequestContext
from django.views.generic.edit import DeletionMixin
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view


logger = logging.getLogger(__name__)

control = Controller()

# Create your views here.

def index(request):
    logger.info("index called")
    context = {
        'request': request,
    }
    return render(request, 'match/index.html', context)

def authenticate_user(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_authenticated:
        login(request, user)
        if username == 'admin':
            return admin_page(request)
        else:
            return match_page(request)
    context = {
        'request': request,
        'error_message': "Authentication failed"
    }
    return render(request, 'match/login.html', context)

def logout_user(request):
    logout(request)
    context = {
        'request': request,
    }
    return render(request, 'match/index.html', context)

@login_required
def match_page(request):
    user = request.user
    logger.debug("user={}".format(user))
    if not user.is_anonymous:
        personList = Person.objects.filter(user=user)
        if len(personList) == 0:
            logger.info("new user added: {}".format(user))
            person = Person(user=user)
            person.save()
    context = {
        'request': request,
        'user': request.user
    }
    return render(request, 'match/match.html', context)

def admin_page(request):
    context = {
        'request': request,
    }
    return render(request, 'match/admin.html', context)

@api_view(['GET'])
def current_user(request):
    user = request.user
    person = Person.objects.get(user=user)
    ser = PersonSer(person)
    return Response(ser.data)

@api_view(['GET'])
def member_groups(request):
    user = request.user
    person = Person.objects.get(user=user)
    groups = Group.objects.filter(people=person)
    ser = GroupUrlSer(groups, many="True", context={"request": request})
    return Response(ser.data)

@api_view(['GET'])
def owner_groups(request):
    user = request.user
    person = Person.objects.get(user=user)
    groups = Group.objects.filter(owner=person)
    ser = GroupUrlSer(groups, many="True", context={"request": request})
    return Response(ser.data)

class PeopleViewSet(viewsets.ModelViewSet):
    """Define view behavior"""
    queryset = Person.objects.all()
    serializer_class = PersonSer
    
class GroupViewSet(viewsets.ModelViewSet,
                    DeletionMixin):
    """Define view behavior"""
    queryset = Group.objects.all()
    serializer_class = GroupUrlSer
    
    def perform_create(self, serializer):
        person = Person.objects.get(user=self.request.user)
        serializer.save(owner=person)
        
    @action(detail=True, methods=["get"])
    def get(self, request, pk=None):
        group = Group.objects.get(id=pk)
        ser = ResultUrlSer(group, context={"request": request})
        return Response(ser.data)
    
    @action(detail=True, methods=["post"])
    def run_match(self, request, pk=None):
        group = Group.objects.get(id=pk)
        result = control.run_match(group)
        ser = ResultUrlSer(result, context={"request": request})
        return Response(ser.data)
    
    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Adding {} to group {}".format(person, group))
        control.add_person_to_group(person, group)
        ser = GroupUrlSer(group, context={"request": request})
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["post"])
    def remove_user_from_group(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Removing {} from group {}".format(person, group))
        control.remove_person_from_group(person, group)
        ser = GroupUrlSer(group, context={"request": request})
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        group = Group.objects.get(id=pk)
        ser = GroupUrlSer(group, context={"request": request})
        return Response(ser.data)
    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultUrlSer
    
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchUrlSer
    
