from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from rest_framework_simplejwt.tokens import RefreshToken


def send_email_with_confirmation_code(user, confirmation_code):
    send_mail(
        subject=f'Сonfirmation code for {user}',
        message=(
            f'Здравствуйте, {user}, навравляем Вам код авторизации'
            f'(confirmation_code) - {confirmation_code}'
        ),
        from_email='from@example.com',
        recipient_list=[user.email],
        fail_silently=False,
    )


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def get_access_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
