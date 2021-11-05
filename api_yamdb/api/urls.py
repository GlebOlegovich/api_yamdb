from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, TitlesViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register('titles', TitlesViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router.urls)),
]
