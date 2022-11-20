from django.core.exceptions import ValidationError


def only_letter_numbers_and_underscore_validator(value):
    for c in value:
        if not c.isalpha() and not c.isdigit() and not c == '_':
            raise ValidationError(f"Ensure this value contains only letters, numbers, and underscore.")
