from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    logger.info("index called")
    context = {}
    return render(request, "match/add_user.html", context)


def add_user(request):
    name = request.POST['name']
    email = request.POST['email']
    logger.info("post: name={}, email={}".format(name, email))
    context = {}
    return render(request, "match/index.html", context)