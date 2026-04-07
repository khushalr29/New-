import re
from ..response import ResponseMessages
from rest_framework import serializers

COUNTRY_PHONE_RULES = { 
    '91': [10],
}


def validate_phone_number(data, *, phone_field="phone_number", code_field="country_number_code"):
    number = data.get(phone_field)
    code = data.get(code_field)

    if code and number:
        if not isinstance(number, (int, str)):
            raise serializers.ValidationError({
                phone_field: ResponseMessages.PHONE_TYPE_INVALID.format(field_name=phone_field.replace('_', ' ').title())
            })

        number_str = str(number).strip()

        if number_str.startswith('+'):
            raise serializers.ValidationError({
                phone_field: ResponseMessages.PHONE_SHOULD_NOT_INCLUDE_PLUS.format(field_name=phone_field.replace('_', ' ').title())
            })

        clean_number = re.sub(r'\D', '', number_str)

        if not clean_number.isdigit():
            raise serializers.ValidationError({
                phone_field: ResponseMessages.PHONE_FORMAT_INVALID.format(field_name=phone_field.replace('_', ' ').title())
            })


        str_code = str(code)
        if str_code not in COUNTRY_PHONE_RULES:
            raise serializers.ValidationError({
                code_field: ResponseMessages.PHONE_PARSE_ERROR.format(error="Unsupported country code")
            })

        valid_lengths = COUNTRY_PHONE_RULES[str_code]
        if len(clean_number) not in valid_lengths:
            raise serializers.ValidationError({
                phone_field: ResponseMessages.PHONE_NOT_POSSIBLE.format(field_name=phone_field.replace('_', ' ').title())
            })

        data[phone_field] = clean_number
        data[code_field] = int(code)

    return data
