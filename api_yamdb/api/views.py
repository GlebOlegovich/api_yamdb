from django.contrib.auth import get_user_model
from rest_framework import filters, serializers, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, UserInfoSerializer, ReviewSerializer, CommentSerializer
from .permissions import AdminOrSuperuser
from reviews.models import Comment, Review, Title
from .permissions import IsUserAnonModerAdmin


User = get_user_model()


class MyPagination(PageNumberPagination):
    page_size = 4


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperuser,)
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserInfoViewSet(APIView):
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserInfoSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            tmp = serializer.save()
            print(tmp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

