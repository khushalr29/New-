import json
import hashlib
from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from ..utils.response import ResponseHandler,ResponseMessages

class DeviceFingerprintMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response
        self.max_attempts_per_device = getattr(settings, 'MAX_LOGIN_ATTEMPTS_DEVICE', 20)
    
    def process_request(self, request):
        
        if not self.should_check_request(request):
            return None
        
        device_fingerprint = self.create_device_fingerprint(request)
        
        if self.is_device_rate_limited(device_fingerprint):            
            return ResponseHandler.json_rate_limited(message=ResponseMessages.TOO_MANY_REQUESTS)
        
        self.record_device_attempt(device_fingerprint)
        return None
    
    def should_check_request(self, request):
        return (request.method == 'POST' and 
                any(url in request.path_info for url in ['login', 'auth']))
    
    def create_device_fingerprint(self, request):
        fingerprint_data = {
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'accept_language': request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
            'accept_encoding': request.META.get('HTTP_ACCEPT_ENCODING', ''),
            'accept': request.META.get('HTTP_ACCEPT', ''),
        }
        
        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]
    
    def is_device_rate_limited(self, device_fingerprint):
        device_key = f'device_attempts_{device_fingerprint}'
        attempts = cache.get(device_key, 0)
        return attempts >= self.max_attempts_per_device
    
    def record_device_attempt(self, device_fingerprint):
        device_key = f'device_attempts_{device_fingerprint}'
        attempts = cache.get(device_key, 0) + 1
        cache.set(device_key, attempts, 3600)