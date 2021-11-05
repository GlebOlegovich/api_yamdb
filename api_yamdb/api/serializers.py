from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Titles, Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
