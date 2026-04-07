from functools import wraps
from rest_framework.response import Response
from .userActivity import log_user_activity

def log_activity(action, resource):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            request = args[1] if len(args) > 1 else None
            user = getattr(request, 'user', None)
            resource_id = kwargs.get('id') or (args[2] if len(args) > 2 else None)

            try:
                response = func(self, *args, **kwargs)
                status = 'success' if isinstance(response, Response) and response.status_code < 400 else 'failed'
                log_user_activity(
                    user=user,
                    action=action,
                    resource=resource,
                    resource_id=resource_id,
                    status=status,
                    request=request,
                    response=response
                )
                return response
            except Exception as e:
                log_user_activity(
                    user=user,
                    action=action,
                    resource=resource,
                    resource_id=resource_id,
                    status='failed',
                    request=request,
                    response=None
                )
                raise e
        return wrapper
    return decorator
