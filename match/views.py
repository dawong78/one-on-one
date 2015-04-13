import logging
from match.algorithm import *
from match.control import Controller
from match.models import *
from match.serializers import *

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route

import os
import logging
import httplib2

from apiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from models import CredentialsModel
from one_on_one import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
logger = logging.getLogger(__name__)

control = Controller()

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Create your views here.

@login_required
def index(request):
    logger.info("index called")
    logger.debug("user={}".format(request.user))
#    REDIRECT_URI = "https://%s%s" % (
#        get_current_site(request).domain, reverse("oauth2:return"))
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/plus.login',
        redirect_uri='http://localhost:5000/oauth2callback')
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=request.user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        logger.info("index: successful login")
#        http = httplib2.Http()
#        http = credential.authorize(http)
#        service = build('plus', 'v1', http=http)
#        activities = service.activities()
#        activitylist = activities.list(collection='public',
#                userId='me').execute()
#        logger.info(activitylist)

        context = {}
        return render(request, "match/index.html", context)

@login_required
def auth_return(request):
    logger.debug("oauth2 callback called")
    if not xsrfutil.validate_token(settings.SECRET_KEY, 
            str(request.REQUEST['state']), request.user):
        logger.debug("bad request")
        return  HttpResponseBadRequest()
    logger.debug("good request")
    FLOW = FlowModel.objects.get(id=request.user).flow
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/match")

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
    
