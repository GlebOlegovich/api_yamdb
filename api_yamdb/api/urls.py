from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserInfoViewSet, CommentViewSet, ReViewSet
from rest_framework.authtoken import views

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReViewSet, TitlesViewSet, UserViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReViewSet, basename='ReViewSet')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='CommentViewSet'
)


urlpatterns = [
    # Важный факт, такие адреса должны быть до подключения роутера!
    path('v1/users/me/', UserInfoViewSet.as_view()),
    path('v1/', include(router.urls)),
]
