<<<<<<< HEAD
from decimal import Context
from django.http import request
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from reviews.models import Category, Title, Genre, Comment, Review
from .permissions import (IsAdminOrReadOnly, AdminOrSuperuser,
                          IsUserAnonModerAdmin)
from .serializers import (CategorySerializer, GenreSerializer,
                          OutputSerializer, InputSerializer,
                          UserSerializer, UserInfoSerializer,
                          ReviewSerializer, CommentSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import TitleFilter
from rest_framework.generics import get_object_or_404
from django.db.models import Avg
import json

User = get_user_model()


class MyPagination(PageNumberPagination):
    page_size = 4

=======
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reviews.models import Category, Comment, Genre, Review, Title

from reviews.models import Category, Comment, Genre, Review, Title
from .filters import TitleFilter
from .permissions import (AdminOrSuperuser, IsAdminOrReadOnly,
                          IsUserAnonModerAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, InputTitleSerializer,
                          OutputTitleSerializer, ReviewSerializer,
                          UserInfoSerializer, UserSerializer)
from .paginators import FourPerPagePagination

User = get_user_model()

>>>>>>> 5cd77ba2e9878adc1972fc6605528422e73bf096

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # https://www.django-rest-framework.org/api-guide/generic-views/#attributes
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOrSuperuser,)
    pagination_class = FourPerPagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        serializer_class=UserInfoSerializer,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
<<<<<<< HEAD
        if serializer.is_valid():
            tmp = serializer.save()
            print(tmp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.get_queryset().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = MyPagination
=======
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@action(detail=True, methods=['GET', 'POST', 'DEL', 'PATCH'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = FourPerPagePagination
>>>>>>> 5cd77ba2e9878adc1972fc6605528422e73bf096
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


@action(detail=True, methods=['LIST', 'POST', 'DEL'])
class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = FourPerPagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_destroy(self, instance):
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return Response(None,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = GenreSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return Response(None,
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = GenreSerializer(instance, data=request.data,
                                     partial=True)
        serializer.is_valid(raise_exception=False)
        self.perform_update(serializer)
        return Response(serializer.data)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year', 'category', 'genre')
    filter_class = TitleFilter
    
    
    def get_rating(self, *args, **kwargs):
        """title = get_object_or_404(Title, id=self.kwargs['title_id'])
        dict = Review.objects.filter(title_id=title).aggregate(
            Avg('score')
            )
        rating = dict.get('score__avg')
        if rating == 0:
            return 'Оценок, пока что, нету...'
        return rating"""
        Title.objects.all().annotate(rating=Avg('reviews__score'))
        id = self.kwargs['id']
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        dict = Review.objects.filter(title__id=self.kwargs['id']).self.aggregate(
            Avg('score')
        )
        print(dict)
        rating = dict.get('score__avg')
        if rating == 0:
            return 'Оценок, пока что, нету...'
        return rating

    """def get_serializer_context(self):
        if self.get_rating() is not type(None):
            return {'rating': self.get_rating()}
        return None"""

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OutputSerializer
        return InputSerializer

class ReViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    queryset = Review.objects.get_queryset().order_by('id')
    serializer_class = ReviewSerializer
    pagination_class = FourPerPagePagination

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return Review.objects.filter(
            title__id=self.kwargs['title_id']).select_related('author')

    def perform_create(self, serializer):
        title = self._get_title()
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    queryset = Comment.objects.get_queryset().order_by('id')
    serializer_class = CommentSerializer
    pagination_class = FourPerPagePagination

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return Comment.objects.filter(review__id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = self._get_review()
        author = get_object_or_404(User, username=self.request.user)
        return serializer.save(author=author, review=review)
