from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        #fields = ()
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
