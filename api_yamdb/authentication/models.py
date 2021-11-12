from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.settings import ROLE, GLOBAL_SETTINGS
from .validators import LowercaseLettersUsernameValidator, NotMeUsername


class User(AbstractUser):
    # Это я хотел, что бы ники были только в нижнем регистре
    # Пытался сделать, что бы ники Nik и nik были бы одним и тем же юзером
    # Но в тестах Test_User ник, так что для тестов оставим как в оригинале
    my_username_validator = LowercaseLettersUsernameValidator()

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text=(
            'Enter a valid username. This value may contain only '
            'lowercase ASCII letters, '
            'numbers, and underscores. Must start with a letter.'
        ),
        validators=[UnicodeUsernameValidator(), NotMeUsername()],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField('email address', unique=True,)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль - права доступа',
        max_length=10,
        choices=ROLE,
        default=GLOBAL_SETTINGS['user']
    )

    @property
    def _is_admin_or_superuser(self):
        return self.role == GLOBAL_SETTINGS['admin'] or self.is_superuser

    @property
    def _is_moderator(self):
        return self.role == GLOBAL_SETTINGS['moderator']

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Юзеры'
        verbose_name = 'Юзер'
