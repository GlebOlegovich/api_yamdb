from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre, through='Genre_title')

    class Meta:
        ordering = ['id']

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

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='genre_titles'
            )
        ]

    def __str__(self):
        return f'"{self.title}" относится к жанру : {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews')
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
        ordering = ['id']
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_field')
        ]

    def __str__(self):
        return self.text


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
        ordering = ['id']
        default_related_name = 'comments'
        verbose_name_plural = 'Коментарии к отзывам'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text
