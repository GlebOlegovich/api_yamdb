from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api.views import CommentViewSet, ReViewSet
from rest_framework.authtoken import views

router = SimpleRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReViewSet, basename='ReViewSet')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='CommentViewSet')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]