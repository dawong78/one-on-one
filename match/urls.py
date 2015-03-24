from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    url(r'^group/(?P<id>[0-9]+)/people/$', views.GroupPeopleView.as_view(), name='group-people'),
    url(r'^$', views.index, name='index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)