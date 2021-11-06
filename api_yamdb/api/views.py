from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Titles, Genre
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          OutputSerializer, InputSerializer)


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
