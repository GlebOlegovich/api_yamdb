from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (AdminOrSuperuser, IsAdminOrReadOnly,
                          IsUserAnonModerAdmin)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, InputSerializer, OutputSerializer,
                          ReviewSerializer, UserInfoSerializer, UserSerializer)

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
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = MyPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def perform_destroy(self, instance):
        instance.delete()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = MyPagination
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
    # Тут еще ругается на подсчет рейтинга... как то надо фиксить
    # Но, я хз как... @ Godleib
    queryset = Title.objects.select_related(
        'category').prefetch_related('genre').all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = MyPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('name', 'year', 'category', 'genre')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OutputSerializer
        return InputSerializer


class ReViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = MyPagination

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
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = MyPagination

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return Comment.objects.filter(review__id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = self._get_review()
        author = get_object_or_404(User, username=self.request.user)
        return serializer.save(author=author, review=review)
