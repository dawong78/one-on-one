from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_on_one.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # REST urls
    url(r'^groups$', views.GroupListView.as_view(), name='groups'),
    url(r'^people/(?P<id>[0-9]+)$', views.PersonView.as_view(), name='add_user'),
    
    # Other urls
    url(r'^create_group$', views.create_group, name='create_group'),
    url(r'^create_group_matches$', views.create_group_matches, name='create_group_matches'),
    url(r'^$', views.index, name='index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)