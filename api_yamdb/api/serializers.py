from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from api_yamdb.settings import ROLE
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )
        optional_fields = ('first_name', 'last_name', 'bio', 'role')


# Так делать вообще нормально?)
class UserInfoSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=ROLE, read_only=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class OutputTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description',
            'genre', 'category', 'rating'
        )

    def get_status(self, obj):
        dict = Review.objects.filter(title_id=int(obj.id)).aggregate(
            Avg('score')
        )
        rating = dict.get('score__avg')
        if rating == 0:
            return 'Оценок, пока что, нету...'
        return rating


class InputTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = timezone.now().year
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
