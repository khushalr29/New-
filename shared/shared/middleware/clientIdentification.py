import uuid
import hashlib
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class ClientIdentificationMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response
        self.cookie_name = getattr(settings, 'CLIENT_ID_COOKIE', 'user_id')
        self.cookie_max_age = getattr(settings, 'CLIENT_ID_COOKIE_AGE', 30 * 24 * 60 * 60)
    
    def process_response(self, request, response):
        
        if not request.COOKIES.get(self.cookie_name):
            client_id = self.generate_client_id(request)
            response.set_cookie(
                self.cookie_name,
                client_id,
                max_age=self.cookie_max_age,
                httponly=True,
                secure=request.is_secure(),
                samesite='Lax'
            )
        
        return response
    
    def generate_client_id(self, request):
        unique_data = f"{uuid.uuid4()}-{request.META.get('HTTP_USER_AGENT', '')}"
        return hashlib.sha256(unique_data.encode()).hexdigest()[:32]
    