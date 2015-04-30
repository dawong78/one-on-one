import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

import os
import logging

logger = logging.getLogger(__name__)

control = Controller()

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Create your views here.

def index(request):
    logger.info("index called")
    logger.debug("user={}".format(request.user))
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('match/index.html',
                             context_instance=context)

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
    
