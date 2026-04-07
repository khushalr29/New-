from django.db.models.fields.related import ForeignKey
from django.core.exceptions import FieldDoesNotExist

def flatten_errors(errors, parent_key=''):
    required_fields = []
    fk_error_fields = []
    type_error_fields = []
    other_errors = []

    required_keywords = {
        "This field is required.",
        "This field may not be blank.",
        "This field may not be null."
    }

    def is_fk_error(msg):
        msg = str(msg)
        return 'does not exist' in msg.lower() or 'invalid pk' in msg.lower()

    def is_type_error(msg):
        msg = str(msg).lower()
        return ('incorrect type' in msg or 
                'expected pk value, received list' in msg or
                'expected' in msg and 'received' in msg)

    def _collect_errors(errs, prefix=''):
        for key, value in errs.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                _collect_errors(value, full_key)
            elif isinstance(value, list):
                for msg in value:
                    msg_str = str(msg)
                    if msg_str in required_keywords:
                        required_fields.append(full_key)
                    elif is_fk_error(msg_str):
                        fk_error_fields.append(full_key)
                    elif is_type_error(msg_str):
                        type_error_fields.append(full_key)
                    else:
                        other_errors.append(f"{full_key}: {msg_str}")
                    break
            else:
                msg_str = str(value)
                if msg_str in required_keywords:
                    required_fields.append(full_key)
                elif is_fk_error(msg_str):
                    fk_error_fields.append(full_key)
                elif is_type_error(msg_str):
                    type_error_fields.append(full_key)
                else:
                    other_errors.append(f"{full_key}: {msg_str}")

    if isinstance(errors, dict):
        _collect_errors(errors, parent_key)
    elif isinstance(errors, list):
        for msg in errors:
            msg_str = str(msg)
            key = parent_key or 'unknown_field'
            if msg_str in required_keywords:
                required_fields.append(key)
            elif is_fk_error(msg_str):
                fk_error_fields.append(key)
            elif is_type_error(msg_str):
                type_error_fields.append(key)
            else:
                other_errors.append(f"{key}: {msg_str}")
            break
    else:
        key = parent_key or 'unknown_field'
        msg_str = str(errors)
        if msg_str in required_keywords:
            required_fields.append(key)
        elif is_fk_error(msg_str):
            fk_error_fields.append(key)
        elif is_type_error(msg_str):
            type_error_fields.append(key)
        else:
            other_errors.append(f"{key}: {msg_str}")

    grouped_errors = []
    
    if required_fields:
        fields_str = ", ".join(required_fields)
        grouped_errors.append(f"{fields_str}: This field is required.")
    
    if fk_error_fields:
        fields_str = ", ".join(fk_error_fields)
        grouped_errors.append(f"{fields_str}: Invalid foreign key.")
    
    if type_error_fields:
        fields_str = ", ".join(type_error_fields)
        grouped_errors.append(f"{fields_str}: Incorrect type.")
    grouped_errors.extend(other_errors)

    return grouped_errors

POSSIBLE_RELATED_LOOKUP_FIELDS = ['name', 'company_name', 'department', 'supplier_name','person_name','gender' ]

def resolve_foreign_key_filters(model, filters: dict) -> dict:
    resolved_filters = {}

    for param, value in filters.items():
        if not value:
            continue

        base_field = param.split('__')[0]

        try:
            field = model._meta.get_field(base_field)

            if isinstance(field, ForeignKey):
                related_model = field.remote_field.model

                if str(value).isdigit():
                    resolved_filters[f"{base_field}__id"] = value
                    continue

                for candidate in POSSIBLE_RELATED_LOOKUP_FIELDS:
                    try:
                        related_model._meta.get_field(candidate)
                        resolved_filters[f"{base_field}__{candidate}"] = value
                        break
                    except FieldDoesNotExist:
                        continue
                else:
                    continue
            else:
                resolved_filters[param] = value

        except FieldDoesNotExist:
            continue

    return resolved_filters
