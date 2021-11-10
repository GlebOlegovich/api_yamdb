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
    if serializer.is_valid():
        valid_date = dict(serializer.validated_data)
        user = get_object_or_404(
            User,
            username__iexact=valid_date['username'].lower()
        )
        if (
            user is not None
            and account_activation_token.check_token(
                user=user,
                token=valid_date['confirmation_code']
            )
        ):
            token = get_access_token_for_user(user)
            return Response({'token': token['access']})
        else:
            return Response(
                {'token': 'Неверный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {'token': 'Ваш код - невалиден!'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_or_create_user(request):
    '''
        Очень вероятно, что это очень убогая вью функция))
    '''
    obj_serializer = UsernameAndEmailObjSerialiser(data=request.data)
    if not obj_serializer.is_valid():
        return Response(
            obj_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(**obj_serializer.validated_data)
    except User.DoesNotExist:
        # я хз, как еще, кроме, как в модели наложить уникальность на email
        model_obj_serializer = UsernameAndEmailModelSerialiser(
            data=request.data
        )
        if not model_obj_serializer.is_valid():
            return Response(
                model_obj_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = model_obj_serializer.save()
    print(user)
    send_email_with_confirmation_code(
        user,
        account_activation_token.make_token(user))
    return Response(request.data)
