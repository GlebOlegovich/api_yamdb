from django.contrib.auth.models import AbstractUser
from django.db import models
from api_yamdb.settings import ROLE


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль - права доступа',
        max_length=1,
        choices=ROLE,
        default='user'
    )


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre_title(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='titles')
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre')

    def __str__(self):
        return f'"{self.title}" относится к жанру : {self.genre}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='genre_titles'
            )
        ]
