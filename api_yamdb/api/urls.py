from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (
    CategoryViewSet, TitlesViewSet,
    GenreViewSet, UserViewSet, UserInfoViewSet,
    CommentViewSet, ReViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitlesViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'users', UserViewSet, basename='users')
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
