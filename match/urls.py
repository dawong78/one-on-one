from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'one_on_one.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
)