from django.core.exceptions import ValidationError


def validate_zero(value):
    if value == 0:
        raise ValidationError("Время приготовления не может быть равно нулю")
