from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserInfoViewSet

app_name = 'urls'

router = DefaultRouter()

router.register(r'users', UserViewSet)
urlpatterns = [
    # Важный факт, такие адреса должны быть до подключения роутера!
    path('v1/users/me/', UserInfoViewSet.as_view()),
    path('v1/', include(router.urls)),
]
