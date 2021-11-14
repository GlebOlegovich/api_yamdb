from datetime import datetime
from django.core.exceptions import ValidationError


def title_year_validator(value):
    if value < 1900 or value > datetime.now().year:
        raise ValidationError(
            ('%(value)s - слишком давно это было, давай что то посвежее'),
            params={'value': value},
        )
