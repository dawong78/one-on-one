import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max
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
    control.sync_user_to_person()
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
    ser = GroupSer(groups, many="True")
    return Response(ser.data)

@api_view(['GET'])
def owner_groups(request):
    user = request.user
    person = Person.objects.get(user=user)
    groups = Group.objects.filter(owner=person)
    ser = GroupSer(groups, many="True")
    return Response(ser.data)

class PeopleViewSet(viewsets.ModelViewSet):
    """Define view behavior"""
    queryset = Person.objects.all()
    serializer_class = PersonSer
    
class GroupViewSet(viewsets.ModelViewSet,
                    DeletionMixin):
    """Define view behavior"""
    queryset = Group.objects.all()
    serializer_class = GroupSer
    
    @action(detail=True, methods=["get"])
    def get(self, request, pk=None):
        group = Group.objects.get(id=pk)
        ser = GroupSer(group)
        return Response(ser.data)
    
    @action(detail=True, methods=["post"])
    def run_match(self, request, pk=None):
        group = Group.objects.get(id=pk)
        result = control.run_match(group)
        ser = ResultSer(result)
        return Response(ser.data)
    
    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Adding {} to group {}".format(person, group))
        control.add_person_to_group(person, group)
        ser = GroupSer(group)
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["post"])
    def add_person(self, request, pk=None):
        person_id = request.query_params.get('person_id')
        group = Group.objects.get(id=pk)
        person = Person.objects.get(id=person_id)
        logger.info("Adding {} to group {}".format(person, group))
        control.add_person_to_group(person, group)
        ser = GroupSer(group)
        return Response(ser.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["post"])
    def remove_person(self, request, pk=None):
        person_id = request.query_params.get('person_id')
        group = Group.objects.get(id=pk)
        person = Person.objects.get(id=person_id)
        logger.info("Removing {} from group {}".format(person, group))
        control.remove_person_from_group(person, group)
        ser = GroupSer(group)
        return Response(ser.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def remove_user_from_group(self, request, pk=None):
        group = Group.objects.get(id=pk)
        person = Person.objects.get(user=request.user)
        logger.info("Removing {} from group {}".format(person, group))
        control.remove_person_from_group(person, group)
        ser = GroupSer(group)
        return Response(ser.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        group = Group.objects.get(id=pk)
        ser = GroupSer(group)
        return Response(ser.data)
    
    @action(detail=True, methods=["delete"])
    def clear_results(self, request, pk=None):
        group = Group.objects.get(id=pk)
        control.clear_group_results(group)
        return Response({})
        
    @action(detail=False, methods=['get'])
    def member_group_ids(self, request, pk=None):
        user = request.user
        person = Person.objects.get(user=user)
        groups = Group.objects.filter(people=person)
        group_ids = []
        for group in groups:
            group_ids.append(group.id)
        return Response(group_ids)
    
    @action(detail=False, methods=['get'])
    def owner_group_ids(self, request, pk=None):
        user = request.user
        person = Person.objects.get(user=user)
        groups = Group.objects.filter(owner=person)
        group_ids = []
        for group in groups:
            group_ids.append(group.id)
        return Response(group_ids)


    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSer

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSer
    