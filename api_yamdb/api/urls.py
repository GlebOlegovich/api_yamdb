from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TitlesViewSet, GenreViewSet, UserViewSet, UserInfoViewSet

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitlesViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # Важный факт, такие адреса должны быть до подключения роутера!
    path('v1/users/me/', UserInfoViewSet.as_view()),
    path('v1/', include(router.urls)),
]
