from django.core.exceptions import ValidationError
import webcolors


def validate_hex(value):
    try:
        valid_value = webcolors.normalize_hex(value)
    except ValueError:
        raise ValidationError(
            f'Цвет {value} не соответствует формату HEX #RRGGBB')
    return valid_value
