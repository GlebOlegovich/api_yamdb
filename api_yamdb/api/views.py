from rest_framework import viewsets
from reviews.models import Title
from reviews.models import Comment, Review
from .serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .permis import IsUserAnonModerAdmin
from django.contrib.auth import get_user_model


User = get_user_model()

class ReViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self._get_title().id
        return Review.objects.filter(title=title)
    
    def perform_create(self, serializer):
        title = self._get_title()
        return serializer.save(author=self.request.user, title = title)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        review_id= self._get_review().id
        return Comment.objects.filter(review_id=review_id)
    
    def perform_create(self, serializer):
        review = self._get_review()
        return serializer.save(author=self.request.user, review = review)
