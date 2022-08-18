import os
from django.core.exceptions import ValidationError


def validate_file_extentions(value):
    ext = os.path.splitext(value.name)[1]
    valid_extention = ['.pdf', '.jpg', '.docx']
    if not ext.lower() in valid_extention:
        raise ValidationError('Unsupported File Type')