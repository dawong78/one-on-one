from django.shortcuts import render
import logging
from models import *
from algorithm import *
from django.db.models import Max

logger = logging.getLogger(__name__)

# Create your views here.

def create_context(error_message=None):
    context = {}
    if not error_message is None:
        context["error_message"] = error_message
    
    groups = Group.objects.all()
    logger.debug("context groups={}".format(groups))
    
    view_groups = []
    for group in groups:
        count = Result.objects.filter(group=group).count()
        matches = []
        if count > 0:
            latest_date = Result.objects.filter(group=group)\
                    .aggregate(Max("date_created"))["date_created__max"]
            logger.debug("latest_date={}".format(latest_date))
            result = Result.objects.get(date_created=latest_date)
            logger.debug("result={}".format(result))
            matches = Match.objects.filter(result=result)
            logger.debug("matches={}".format(matches))
        view_group = ViewGroup(group=group, matches=matches)
        view_groups.append(view_group)
    context["groups"] = view_groups
    return context

def index(request):
    logger.info("index called")
    context = create_context()
    return render(request, "match/index.html", context)


def add_user(request):
    """Add a new user to a group
    Create the user, if he/she does not exist
    
    Expected parameters
    name - name of user
    email - email of user
    group - group to join
    """
    name = request.POST["name"]
    email = request.POST["email"]
    group = request.POST["group"]
    logger.info("post: name={}, email={}, group={}".format(name, email, group))
    personList = Person.objects.filter(name=name,email=email)
    person = None
    if len(personList) == 0:
        # New person
        logger.debug("Creating new user: {}".format(person))
        person = Person.objects.create(name=name,email=email)
        person.save()
    else:
        person = personList[0]
    group = Group.objects.get(name=group)
    if group.people is None:
        group.people = []
    group.people.add(person)
    group.save()
    context = create_context()
    return render(request, "match/index.html", context)

def create_group(request):
    """Create new group"""
    name = request.POST["name"]
    groupList = Group.objects.filter(name=name)
    logger.debug("groupList={}".format(groupList))
    error = None
    if len(groupList) > 0:
        log.debug("Group already exists: {}".format(name))
        error = "Group name already exists"
    else:
        logger.debug("Creating group: {}".format(name))
        group = Group.objects.create(name=name)
        group.save()
        logger.info("Created group {}".format(name))
    context = create_context(error)
    return render(request, "match/index.html", context)
    
def create_group_matches(request):
    """Create new matches for a group"""
    group_name = request.POST["group_name"]
    logger.debug("Creating matches for group {}".format(group_name))
    controller = Controller()
    match_results = controller.run_match(group_name)
    logger.debug("Match results: {}".format(match_results))
    context = create_context()
    return render(request, "match/index.html", context)
    