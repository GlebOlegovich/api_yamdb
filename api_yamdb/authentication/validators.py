from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class MyUsernameValidator(validators.RegexValidator):
    """
    Validator for usernames.\n
    - Only ASCII lowercase letters, numbers and underscore are supported.
    - Must start with a letter.
    """
    regex = r'^[a-z][a-z0-9_]+$'
    message = (
        'Enter a valid username. This value may contain only '
        'lowercase ASCII letters, '
        'numbers, and underscores. Must start with a letter.'
    )
    flags = 0
