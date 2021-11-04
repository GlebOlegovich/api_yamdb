# from rest_framework import serializers
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from .validators import MyUsernameValidator


class UsernameAndEmailObjSerialiser(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[MyUsernameValidator()]
    )
    email = serializers.EmailField()

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError("'me' - недопустимое имя!")
        return username


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
        try:
            User.objects.get(username__iexact=username.lower())
            raise serializers.ValidationError(f'Пользователь с ником {username} уже есть')
        except User.DoesNotExist:
            pass
        return username

    def validate_email(self, email):
        try:
            User.objects.get(email__iexact=email.lower())
            raise serializers.ValidationError(f'Пользователь с почтой {email} уже есть')
        except User.DoesNotExist:
            pass
        return email

    class Meta:
        model = User
        fields = ('username', 'email')
        # Пока что не оч понял, какая нам уникальность нужна, осталю
        # уникальнымипо отдельности пока что, по идее - так
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=model.objects.all(),
        #         fields=('username', 'email'),
        #         message='Пользователь с такими данными уже заресистирован'
        #     )
        # ]


class GetTokenSerialiser(serializers.Serializer):

    username = serializers.CharField(
        max_length=150,
        validators=[MyUsernameValidator()]
    )
    confirmation_code = serializers.CharField()
