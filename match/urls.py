from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^current_user$', views.current_user, name="current-user"),
    url(r'^member_groups$', views.member_groups, name="member-groups"),
    url(r'^owner_groups$', views.owner_groups, name="owner-groups")
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)