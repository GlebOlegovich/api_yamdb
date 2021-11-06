from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserInfoViewSet, CommentViewSet, ReViewSet
from rest_framework.authtoken import views

app_name = 'urls'

router = DefaultRouter()


router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReViewSet, basename='ReViewSet')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='CommentViewSet')
urlpatterns = [
    # Важный факт, такие адреса должны быть до подключения роутера!
    path('v1/users/me/', UserInfoViewSet.as_view()),
    path('v1/', include(router.urls)),
]
