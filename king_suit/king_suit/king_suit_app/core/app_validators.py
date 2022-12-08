from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('The name must consist only alphabet letters (a-z)! Please try again!')


def validate_file_size(image_obj):
    if image_obj.size > 5242880:
        raise ValidationError('The maximum file size that can be uploaded is 5MB')
