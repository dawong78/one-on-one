from django.urls import include, path, re_path
# from django.contrib import admin

from rest_framework import routers

from match import views


router = routers.DefaultRouter()
router.register(r'people', views.PeopleViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'matches', views.MatchViewSet)


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^match/rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('match/', include('match.urls')),
    # path('admin/', include(admin.site.urls)),
]
