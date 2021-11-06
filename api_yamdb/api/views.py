from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import filters, serializers, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Titles, Genre, Comment, Review
from .permissions import IsAdminOrReadOnly, AdminOrSuperuser
from .serializers import (CategorySerializer, GenreSerializer,
                          OutputSerializer, InputSerializer,
                          UserSerializer, UserInfoSerializer,
                          ReviewSerializer, CommentSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OutputSerializer
        return InputSerializer


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
