from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from match import views


router = routers.DefaultRouter()
router.register(r'people', views.PeopleViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'matches', views.MatchViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_on_one.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^match/rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^match/', include('match.urls', namespace="match")),
    url(r'^admin/', include(admin.site.urls)),
)
