from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .validators import LowercaseLettersUsernameValidator, NotMeUsername

User = get_user_model()


class UsernameAndEmailObjSerialiser(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        # Тут тоже убираем, потому что в модели юзера убрали валидатор
        # validators=[LowercaseLettersUsernameValidator()]
        validators=[NotMeUsername()]
    )
    email = serializers.EmailField()

    # Не знаю, как лучше, так, или как выше...
    # def validate_username(self, username):
    #     if username.lower() == 'me':
    #         raise serializers.ValidationError("'me' - недопустимое имя!")
    #     return username


class UsernameAndEmailModelSerialiser(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Недоступный email!')
        ]
    )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError("'me' - недопустимое имя!")

        if User.objects.filter(
            username__iexact=username.lower()
        ).exists():
            print('ewffwefw')
            raise serializers.ValidationError(
                f'Пользователь с ником {username} уже есть'
            )
        print(f'Принт из сериализатора {username}')
        return username

    def validate_email(self, email):
        if User.objects.filter(
            email__iexact=email.lower()
        ).exists():
            print('ewew')
            raise serializers.ValidationError(
                f'Пользователь с почтой {email} уже есть'
            )
        return email

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerialiser(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
        validators=[LowercaseLettersUsernameValidator()]
    )
    confirmation_code = serializers.CharField()
