from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.settings import ROLE

from .validators import MyUsernameValidator, NotMeUsername


class User(AbstractUser):
    ADMIN = 'admin'
    # Это я хотел, что бы ники были только в нижнем регистре
    # Пытался сделать, что бы ники Nik и nik были бы одним и тем же юзером
    # Но в тестах Test_User ник, так что для тестов оставим как в оригинале
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
        # validators=[my_username_validator],
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
        default='user'
    )

    def _is_admin_or_superuser(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        # Странно, я думал по дефолту они сортятся по id, но когда
        # пагинацию накинул - выдало, что неотсортированно
        ordering = ['id']
