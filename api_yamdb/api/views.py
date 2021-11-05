# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters

from reviews.models import Category, Titles, Genre
# from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitlesSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    # permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    # permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.delete()


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = [IsAdminOrReadOnly]
