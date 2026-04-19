from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from match import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^current_user$', views.current_user, name="current-user"),
    re_path(r'^member_groups$', views.member_groups, name="member-groups"),
    re_path(r'^owner_groups$', views.owner_groups, name="owner-groups")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)