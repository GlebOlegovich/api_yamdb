from django.contrib.auth import get_user_model
from rest_framework import serializers
from api_yamdb.settings import ROLE


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )
        read_only_fields = ('role',)
        optional_fields = ('first_name', 'last_name', 'bio', 'role')

# Так делать вообще нормально?)
class UserInfoSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=ROLE, read_only=True)
