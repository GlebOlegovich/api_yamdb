from django.core.exceptions import ValidationError
from django.http import request
from rest_framework import serializers
import datetime as dt
from django.contrib.auth import get_user_model
from api_yamdb.settings import ROLE
from reviews.models import Category, Titles, Genre, Comment, Review
from rest_framework.generics import get_object_or_404
from django.db.models import Avg
from rest_framework.fields import CurrentUserDefault
from rest_framework.response import Response
from rest_framework import status

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


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class OutputSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')

    def get_status(self, obj):
        dict = Review.objects.filter(title_id=int(obj.id)).aggregate(Avg('score'))
        rating = dict.get('score__avg')
        if rating == 0:
            rating = 'None'
            return rating
        return rating

class InputSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год!')
        return value

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def create(self, validated_data):
        author = validated_data.get('author')
        title = validated_data.get('title')
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError()
        return Review.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)