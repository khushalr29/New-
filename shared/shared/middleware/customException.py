from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        if isinstance(response.data, dict):
            
            first_error = next(iter(response.data.values()))
            
            if isinstance(first_error, list):
                first_error = first_error[0]
                
            if "Invalid foreign key" in str(first_error):
                field_name = next(iter(response.data.keys()))
                first_error = f"Invalid data provided for {field_name}."

            response.data = {
                'success': False,
                'message': first_error
            }
        else:
            response.data = {
                'success': False,
                'message': response.data
            }

    return response
