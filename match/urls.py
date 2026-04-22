from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from match import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='match/login.html'), name='login'),
    re_path(r'^$', views.match_page, name='match'),
    path('logout', views.logout_user, name='logout'),
    re_path(r'^current_user$', views.current_user, name="current-user"),
    re_path(r'^member_groups$', views.member_groups, name="member-groups"),
    re_path(r'^owner_groups$', views.owner_groups, name="owner-groups"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)