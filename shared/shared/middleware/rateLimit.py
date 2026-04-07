import re
import time
import uuid
import hmac
import logging
import hashlib
from django.urls import resolve
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from ..utils.response import ResponseHandler,ResponseMessages

logger = logging.getLogger(__name__)

class InMemoryCache:
    _instance = None
    _cache = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get(self, key, default=None):
        item = self._cache.get(key)
        if item is None:
            return default
        
        value, expiry = item
        if expiry and time.time() > expiry:
            del self._cache[key]
            return default
        return value
    
    def set(self, key, value, timeout=None):
        expiry = time.time() + timeout if timeout else None
        self._cache[key] = (value, expiry)
        self._cleanup()
    
    def delete(self, key):
        if key in self._cache:
            del self._cache[key]
    
    def ttl(self, key):
        item = self._cache.get(key)
        if item is None:
            return None
        
        value, expiry = item
        if expiry is None:
            return None
        
        remaining = expiry - time.time()
        return int(remaining) if remaining > 0 else 0
    
    def _cleanup(self):
        if len(self._cache) > 10000:
            now = time.time()
            expired_keys = [
                k for k, (v, exp) in self._cache.items() 
                if exp and now > exp
            ]
            for key in expired_keys:
                del self._cache[key]

class GlobalRateLimitMiddleware(MiddlewareMixin):
    DEFAULT_RATE_LIMITS = {
        'GET': {'limit': 15, 'period': 1},
        'POST': {'limit': 10, 'period': 5},
        'PUT': {'limit': 10, 'period': 5},
        'PATCH': {'limit': 10, 'period': 5},
        'DELETE': {'limit': 10, 'period': 5},
    }
    
    BLOCK_PERIOD = 3 * 60
    API_PREFIX = '/api/v1/'
    WHITELISTED_IPS = []
    SECRET_KEY = getattr(settings, 'RATE_LIMIT_SECRET_KEY', settings.SECRET_KEY)
    CACHE_PREFIX = 'rate_limit'
    CACHE_TIMEOUT = 3600
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = InMemoryCache()

    def process_request(self, request):
        path = request.path
        if not path.startswith(self.API_PREFIX):
            return None

        content_length_valid, error_response = self.validate_content_length(request)
        if not content_length_valid:
            return error_response

        client_ip = self.get_client_ip(request)
        if client_ip in self.WHITELISTED_IPS:
            return None

        user_id = self.get_user_id_from_cookie(request)
        if not user_id:
            user_id = self.generate_user_id(request)
            
        rate_config = self.get_rate_limit_config(request)
        if not rate_config:
            return None
        
        endpoint_key = self.get_endpoint_key(request)
        
        rate_limit_key = f"{self.CACHE_PREFIX}:{user_id}:{endpoint_key}"
        ip_rate_limit_key = f"{self.CACHE_PREFIX}:ip:{client_ip}:{endpoint_key}"
        
        if self.is_rate_limited(rate_limit_key, rate_config):
            return ResponseHandler.json_rate_limited(message=ResponseMessages.TOO_MANY_REQUESTS)

        if self.is_rate_limited(ip_rate_limit_key, rate_config):
            return ResponseHandler.json_rate_limited(message=ResponseMessages.TOO_MANY_REQUESTS)

        self.record_request(rate_limit_key, rate_config)
        self.record_request(ip_rate_limit_key, rate_config)
        
        if not request.COOKIES.get('user_id'):
            request.user_id = user_id

        return None

    def validate_content_length(self, request):
        try:
            if request.method in ['POST', 'PUT', 'PATCH']:
                content_length = request.META.get('CONTENT_LENGTH')
                if content_length:
                    try:
                        expected_length = int(content_length)
                        actual_length = len(request.body)
                        
                        if expected_length != actual_length:
                            error_msg = (
                                f"Content-Length header ({expected_length} bytes) "
                                f"does not match actual body length ({actual_length} bytes). "
                                f"Please ensure your request is properly formatted."
                            )
                            logger.warning(
                                f"Content-Length mismatch for {request.path}: "
                                f"expected {expected_length}, got {actual_length}"
                            )
                            return False, self._create_error_response(error_msg, 400)
                    except ValueError as e:
                        error_msg = "Invalid Content-Length header value"
                        logger.error(f"Invalid Content-Length header: {e}")
                        return False, self._create_error_response(error_msg, 400)
                    except Exception as e:
                        error_msg = "Error reading request body"
                        logger.error(f"Error reading request body: {e}")
                        return False, self._create_error_response(error_msg, 400)
            
            return True, None
            
        except Exception as e:
            error_msg = "Error validating request"
            logger.error(f"Error validating content length: {e}")
            return False, self._create_error_response(error_msg, 400)
    
    def _create_error_response(self, message, status_code=400):
        from django.http import JsonResponse
        
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": None
            },
            status=status_code
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_rate_limited(self, cache_key, rate_config):
        try:
            block_key = f"{cache_key}:blocked"
            if self.cache.get(block_key):
                return True

            request_data = self.cache.get(cache_key, [])
            now_ts = time.time()
            
            recent_requests = [
                t for t in request_data 
                if t > now_ts - rate_config['period']
            ]
            
            if len(recent_requests) >= rate_config['limit']:
                self.cache.set(block_key, True, self.BLOCK_PERIOD)
                self.cache.delete(cache_key)
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return False

    def record_request(self, cache_key, rate_config):
        try:
            request_data = self.cache.get(cache_key, [])
            now_ts = time.time()
            
            recent_requests = [
                t for t in request_data 
                if t > now_ts - rate_config['period']
            ]
            
            recent_requests.append(now_ts)
            self.cache.set(cache_key, recent_requests, self.CACHE_TIMEOUT)
        except Exception as e:
            logger.error(f"Error recording request: {e}")

    def get_remaining_block_time(self, cache_key):
        try:
            block_key = f"{cache_key}:blocked"
            ttl = self.cache.ttl(block_key)
            
            if ttl and ttl > 0:
                minutes = int(ttl // 60)
                seconds = int(ttl % 60)
                return {
                    'lock_time': f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s",
                    'remaining_seconds': int(ttl)
                }
        except Exception as e:
            logger.error(f"Error getting remaining block time: {e}")
        
        return {'lock_time': "Please try again later", 'remaining_seconds': 0}

    def get_endpoint_key(self, request):
        try:
            resolved = resolve(request.path_info)
            endpoint_name = resolved.url_name
            method = request.method.upper()
            
            if endpoint_name:
                sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '', endpoint_name)
                return f"{sanitized_name}:{method}"
            else:
                clean_path = re.sub(r'[^a-zA-Z0-9_-]', '', request.path_info.strip('/').replace('/', '_'))
                return f"path_{clean_path}:{method}" if clean_path else f"root:{method}"
                
        except Exception as e:
            logger.warning(f"Error resolving endpoint for {request.path_info}: {e}")
            clean_path = re.sub(r'[^a-zA-Z0-9_-]', '', request.path_info.strip('/').replace('/', '_'))
            return f"path_{clean_path}:{request.method.upper()}" if clean_path else f"root:{request.method.upper()}"

    def get_rate_limit_config(self, request):
        try:
            method = request.method.upper()
            config = self.DEFAULT_RATE_LIMITS.get(method)
            if not config:
                logger.warning(f"No rate limit config for method {method}, using GET defaults")
                return self.DEFAULT_RATE_LIMITS['GET']
            return config
            
        except Exception as e:
            logger.error(f"Error getting rate limit config: {e}")
            return self.DEFAULT_RATE_LIMITS['GET']

    def get_user_id_from_cookie(self, request):
        try:
            user_id_signed = request.COOKIES.get('user_id')
            if user_id_signed:
                user_id = self.verify_signature(user_id_signed)
                if user_id:
                    return user_id
        except Exception as e:
            logger.warning(f"Invalid user_id cookie: {e}")
        return None

    def set_user_id_cookie(self, response, user_id, request):
        user_id_str = str(user_id)
        signed_user_id = self.sign_data(user_id_str)
        response.set_cookie(
            'user_id', 
            signed_user_id, 
            max_age=60*60*24*365,
            httponly=True, 
            secure=not settings.DEBUG,
            samesite='Lax'
        )

    def generate_user_id(self, request):
        unique_data = f"{uuid.uuid4()}-{request.META.get('HTTP_USER_AGENT', '')}-{time.time()}"
        user_id = hashlib.sha256(unique_data.encode()).hexdigest()[:32]
        return user_id

    def sign_data(self, data):
        if not isinstance(data, str):
            data = str(data)
        signature = hmac.new(
            self.SECRET_KEY.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{data}.{signature}"

    def verify_signature(self, signed_data):
        try:
            parts = signed_data.rsplit('.', 1)
            if len(parts) != 2:
                return None
            
            data, signature = parts
            expected_signature = hmac.new(
                self.SECRET_KEY.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if hmac.compare_digest(signature, expected_signature):
                return data
        except Exception as e:
            logger.warning(f"Error verifying signature: {e}")
        return None

    def process_response(self, request, response):
        if hasattr(request, 'user_id') and request.user_id:
            self.set_user_id_cookie(response, request.user_id, request)

        return response