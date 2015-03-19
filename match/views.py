import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.http import Http404
from django.shortcuts import render, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)
control = Controller()

# Create your views here.

def index(request):
    logger.info("index called")
    error_message = request.session.get("error_message", None)
    request.session["error_message"] = None
    context = create_context(error_message)
    return render(request, "match/index.html", context)

def create_context(error_message=None):
    context = {}
    if not error_message is None:
        context["error_message"] = error_message
    view_groups = control.get_view_groups()
    context["groups"] = view_groups
    return context

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
    controller = Controller()
    match_results = controller.run_match(group_name)
    logger.debug("Match results: {}".format(match_results))
    return redirect("/match")
    

class GroupListView(APIView):
    """ List all the groups """
    def get(self, request, format=None):
        """
        Get all the groups and their current matches
        """
        groups = control.get_view_groups()
        ser = ViewGroupSer(groups, many=True)
        return Response(ser.data)

class PeopleView(APIView):
    """Add a new person"""
    
    def post(self, request, format=None):
        ser = PersonSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PersonView(APIView):
    """Retrieve, update or delete a person instance"""
    
    def get_person(self, id):
        try:
            return Person.objects.get(id=id)
        except Person.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        person = self.get_person(id)
        ser = PersonSer(person)
        return Response(ser.data)
    
    def put(self, request, id, format=None):
        person = self.get_person(id)
        ser = PersonSer(person, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        person = self.get_person(id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
