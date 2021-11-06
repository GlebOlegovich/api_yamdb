from django.contrib.auth import get_user_model
from rest_framework import serializers
from api_yamdb.settings import ROLE
from reviews.models import Comment, Review


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
