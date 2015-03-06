from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_on_one.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create_group$', views.create_group, name='create_group'),
    url(r'^add_user$', views.add_user, name='add_user'),
    url(r'^create_group_matches$', views.create_group_matches, name='create_group_matches'),
    url(r'^$', views.index, name='index'),
)
