from datetime import datetime


def title_year_validator(value):
    if value < 1900 or value > datetime.now().year:
        raise value.ValidationError(
            ('%(value)s is not a correcrt year!'),
            params={'value': value},
        )
