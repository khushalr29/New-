import re
from django.db import models
from django.db.models import Q
from rest_framework import serializers
from ..response import ResponseMessages
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import FieldDoesNotExist
from rest_framework.validators import UniqueValidator

def validate_name(value, field_name="This field"):
    if not value or not value.strip():
        return value

    value = value.strip()

    if len(value) < 3:
        raise ValidationError(ResponseMessages.NAME_TOO_SHORT.format(field_name=field_name))
    if value.startswith('.') or value.endswith('.'):
        raise ValidationError(ResponseMessages.NAME_START_END_DOT.format(field_name=field_name))
    if not re.match(r'^[A-Za-z]', value):
        raise ValidationError(ResponseMessages.NAME_START_LETTER.format(field_name=field_name))
    if not re.fullmatch(r'[A-Za-z0-9 ._-]+', value):
        raise ValidationError(ResponseMessages.NAME_INVALID_CHARS.format(field_name=field_name))
    return value

def validate_adhar_number(value):
    if not re.fullmatch(r'\d{12}', value):
        raise ValidationError("Aadhaar number must be exactly 12 digits.")

    if value[0] in ['0', '1']:
        raise ValidationError("Aadhaar number cannot start with 0 or 1.")

    if value == value[0] * 12:
        raise ValidationError("Invalid Aadhaar: all digits cannot be the same.")

    if value in ['123456789012', '012345678901']:
        raise ValidationError("Invalid Aadhaar: sequential numbers not allowed.")

def validate_domain(value):
    value = value.strip()
    pattern = r'^https:\/\/([a-z0-9\-]+)\.hrms\.in$'
    if not re.match(pattern, value):
        raise ValidationError(ResponseMessages.DOMAIN_INVALID_FORMAT)
    return value

def validate_address(value, field_name='This field', allow_at=False):
    if value is None:
        return value
    cleaned = value.strip()
    if not cleaned:
        return value
    if len(cleaned) < 3:
        raise ValidationError(ResponseMessages.ADDRESS_TOO_SHORT.format(field_name=field_name))
    if not re.search(r'[a-zA-Z]', cleaned):
        raise ValidationError(ResponseMessages.ADDRESS_ALPHA_REQUIRED.format(field_name=field_name))
    if re.fullmatch(r'[^a-zA-Z@]+', cleaned):
        raise ValidationError(ResponseMessages.ADDRESS_SPECIAL_ONLY.format(field_name=field_name))
    if not allow_at:
        if cleaned.startswith('@') or cleaned.endswith('@'):
            raise ValidationError(ResponseMessages.ADDRESS_START_END_AT.format(field_name=field_name))
        allowed_chars = "letters, numbers, spaces, , . - & / ' ( )"
        allowed_pattern = r'[^\w\s,.\-&/\'()]'
    else:
        allowed_chars = "letters, numbers, spaces, , @, . - & / ' ( )"
        allowed_pattern = r'[^\w\s,@.\-&/\'()]'

    if re.search(allowed_pattern, cleaned):
        raise ValidationError(ResponseMessages.ADDRESS_INVALID_CHARACTERS.format(
            field_name=field_name, allowed_chars=allowed_chars))

    if re.search(r'[\u263a-\U0001f645]|\ud83c|\ud83d', cleaned):
        raise ValidationError(ResponseMessages.ADDRESS_EMOJI_NOT_ALLOWED.format(field_name=field_name))

    if re.search(r'[<>^$*#{}[\]\\`~|]', cleaned):
        raise ValidationError(ResponseMessages.ADDRESS_DISALLOWED_SPECIALS.format(field_name=field_name))

    return cleaned

def validate_room_number(value):
    value = str(value).strip()
    if not re.fullmatch(r'^[A-Za-z0-9\- ]+$', value):
        raise ValidationError(ResponseMessages.ROOM_INVALID)
    return value


def validate_char_field(value, field_name='This field', min_length=1, max_length=255, allow_special=False):
    if value is None:
        return value
    value = value.strip()
    if not value:
        raise ValidationError(ResponseMessages.CHAR_FIELD_EMPTY.format(field_name=field_name))
    if len(value) < min_length:
        raise ValidationError(ResponseMessages.CHAR_FIELD_TOO_SHORT.format(field_name=field_name, min_length=min_length))
    if len(value) > max_length:
        raise ValidationError(ResponseMessages.CHAR_FIELD_TOO_LONG.format(field_name=field_name, max_length=max_length))
    if not allow_special:
        if not re.match(r'^[A-Za-z0-9 _./%()-]+$', value):
            raise ValidationError(ResponseMessages.CHAR_FIELD_INVALID_CHARS.format(field_name=field_name))
    return value

def validate_integer_field(value, field_name='This field', min_value=None, max_value=None):
    if value is None:
        return value 
    try:
        value = int(value)
    except (ValueError, TypeError):
        raise ValidationError(ResponseMessages.INTEGER_REQUIRED.format(field_name=field_name))

    if min_value is not None and value < min_value:
        raise ValidationError(ResponseMessages.INTEGER_TOO_SMALL.format(field_name=field_name, min_value=min_value))

    if max_value is not None and value > max_value:
        raise ValidationError(ResponseMessages.INTEGER_TOO_LARGE.format(field_name=field_name, max_value=max_value))

    return value

def validate_email(self, email):
    email_validator = EmailValidator()
    
    try:
        email_validator(email)
    except ValidationError:
        raise ValidationError(ResponseMessages.INVALID_EMAIL)
    
    return email

def validate_required_fields(attrs, instance, required_fields, field_message=None):
    errors = {}

    for field in required_fields:
        value = attrs.get(field) or getattr(instance, field, None)
        if not value:
            display_message = (
                field_message.get(field, field.replace('_', ' ').title())
                if field_message else field.replace('_', ' ').title()
            )
            errors[field] = [ResponseMessages.field_required(display_message)]

    if errors:
        raise serializers.ValidationError(errors)

#Unique True 
class CaseInsensitiveUniqueValidator(UniqueValidator):
    def __init__(self, queryset, fields=None, message=None):
        self.queryset = queryset
        self.fields = fields or []
        self.custom_message = message
        super().__init__(queryset=queryset)

    def __call__(self, value, serializer_field):
        model = self.queryset.model
        instance = serializer_field.parent.instance
        field_name = serializer_field.field_name

        fields = self.fields or [field_name]
        for field in fields:
            if field != field_name:
                continue 

            try:
                model_field = model._meta.get_field(field)
            except FieldDoesNotExist:
                continue

            val = value

            qset = self.queryset
            if instance:
                qset = qset.exclude(pk=instance.pk)

            if 'deleted_by' in [f.name for f in model._meta.fields]:
                qset = qset.filter(deleted_by__isnull=True)

            if model_field.is_relation:
                filter_kwargs = {field: val}
            else:
                filter_kwargs = {f"{field}__iexact": val}

            if qset.filter(**filter_kwargs).exists():
                readable_name = field.replace('_', ' ').capitalize()
                message = self.custom_message or f"{readable_name} already exists."
                raise ValidationError(message)

# for case insensitive unique_together 
class CaseInsensitiveUniqueTogetherValidator:
    def __init__(self, model, fields):
        self.model = model
        self.fields = fields

    def __call__(self, attrs, serializer):
        filters = Q()

        for field in self.fields:
            value = attrs.get(field)
            if value is None and serializer.instance:
                value = getattr(serializer.instance, field)

            if value is not None:
                try:
                    model_field = self.model._meta.get_field(field)
                except FieldDoesNotExist:
                    continue

                if isinstance(model_field, models.ForeignKey):
                    filters &= Q(**{f"{field}": value})
                else:
                    filters &= Q(**{f"{field}__iexact": value})

        if serializer.instance:
            filters &= ~Q(pk=serializer.instance.pk)

        # Dynamically check for field existence before filtering
        model_fields = [field.name for field in self.model._meta.fields]

        if 'deleted_by' in model_fields:
            filters &= Q(deleted_by__isnull=True)
        if 'is_deleted' in model_fields:
            filters &= Q(is_deleted=False)
        if 'deleted_at' in model_fields:
            filters &= Q(deleted_at__isnull=True)
        if 'is_active' in model_fields:
            filters &= Q(is_active=True)

        if self.model.objects.filter(filters).exists():
            field_str = self.fields[0].replace('_', ' ').capitalize()
            raise ValidationError({field_str: "already exists"})
