from django.contrib.auth.models import AbstractUser
from django.db import models
from api_yamdb.settings import ROLE
from .validators import MyUsernameValidator


class User(AbstractUser):
    my_username_validator = MyUsernameValidator()
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=(
            'Enter a valid username. This value may contain only '
            'lowercase ASCII letters, '
            'numbers, and underscores. Must start with a letter.'
        ),
        validators=[my_username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField('email address', blank=True, unique=True,)
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


# class ConfirmationCodeOfUser(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         unique=True,
#         related_name='confirmation_code')
#     confirmation_code = models.CharField(max_length=200, blank=True)
