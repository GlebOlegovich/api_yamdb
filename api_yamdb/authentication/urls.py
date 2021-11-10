from django.urls import path

from authentication.views import get_or_create_user, get_token

app_name = 'authentication'

urlpatterns = [
    path('signup/', get_or_create_user, name='get_or_create_user'),
    path('token/', get_token, name='get_token'),
]
