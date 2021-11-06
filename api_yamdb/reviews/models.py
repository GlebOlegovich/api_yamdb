from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
<<<<<<< HEAD:api_yamdb/reviews/models.py
=======
from api_yamdb.settings import ROLE
>>>>>>> gera:api_yamdb/yamdb/models.py


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    # Надо потом ограничения что ли наложить...
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
        Title,
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


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]

    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'comments'
        verbose_name_plural = 'Коментарии к отзывам'
        verbose_name = 'Коментарий к отзыву'
