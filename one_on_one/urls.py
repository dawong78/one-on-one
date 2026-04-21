from django.urls import include, path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
