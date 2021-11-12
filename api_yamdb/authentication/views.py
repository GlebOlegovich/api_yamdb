from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .core import (account_activation_token, get_access_token_for_user,
                   send_email_with_confirmation_code)
from .models import User
from .serializers import (GetTokenSerialiser, UsernameAndEmailModelSerialiser,
                          UsernameAndEmailObjSerialiser)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = GetTokenSerialiser(data=request.data)
    if serializer.is_valid(raise_exception=True):
        valid_data = dict(serializer.validated_data)
        user = get_object_or_404(
            User,
            username__iexact=valid_data['username'].lower()
        )
        if (
            account_activation_token.check_token(
                user=user,
                token=valid_data['confirmation_code']
            )
        ):
            token = get_access_token_for_user(user)
            return Response({'token': token['access']})
        else:
            return Response(
                {'token': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_or_create_user(request):
    '''
        Очень вероятно, что это очень убогая вью функция))
    '''
    obj_serializer = UsernameAndEmailObjSerialiser(data=request.data)
    obj_serializer.is_valid(raise_exception=True)

    try:
        # Делал так, на случай, ну мало ли, у нас будет
        # косяк и ник будет не уникальным, так хоть
        # еще по email найдем того самого)))
        # user = User.objects.get(**obj_serializer.validated_data)

        # Тут два варика или искать по юзернейму и потом проводить
        # сериализацию данных, что бы email был уникальным,
        # НОВАЯ ЗАПИСЬ НЕ СОЗДАЕТСЯ, но ответ 200
        # (возвращаем то что нам дали на вход), а не 400...
        user = User.objects.get(
            username=obj_serializer.validated_data['username']
        )
        if user.email != request.data['email']:
            raise User.DoesNotExist
        # model_obj_serializer = UsernameAndEmailModelSerialiser(
        #     data=request.data
        # )
        # model_obj_serializer.is_valid(raise_exception=True)
    except User.DoesNotExist:
        model_obj_serializer = UsernameAndEmailModelSerialiser(
            data=request.data
        )
        model_obj_serializer.is_valid(raise_exception=True)
        user = model_obj_serializer.save()
        print(f'Принт из вью {user}')

    print(request.data)
    # send_email_with_confirmation_code(
    #     user,
    #     account_activation_token.make_token(user))
    return Response(request.data)
