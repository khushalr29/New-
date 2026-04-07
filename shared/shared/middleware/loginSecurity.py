import uuid
import json
import time
import hashlib
import logging
from datetime import date
from ..models import User
from django.urls import resolve
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.deprecation import MiddlewareMixin
from ..utils.response import ResponseHandler,ResponseMessages

logger = logging.getLogger('security')

class EmailLoginSecurityMiddleware(MiddlewareMixin):
    @staticmethod
    def check_company_plan_active(email):
        try:
            user = User.objects.select_related('company').get(email=email)
        except User.DoesNotExist:
            return None
        
        if user.account_type != 'company_super_admin':
            return None

        company = user.company
        if not company:
            return None

        today = date.today()
        if company.plan_activation_date and company.plan_activation_date > today:
            return f"Your plan will activate on {company.plan_activation_date.strftime('%Y-%m-%d')}."
        if company.subscription_end_date and company.subscription_end_date < today:
            return "Your subscription has expired."

        return None
    
    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response
        
        self.cookie_name = getattr(settings, 'LOGIN_SECURITY_COOKIE', 'user_id')
        self.cookie_max_age = getattr(settings, 'LOGIN_SECURITY_COOKIE_AGE', 30 * 24 * 60 * 60)
        self.max_attempts_per_email = getattr(settings, 'MAX_LOGIN_ATTEMPTS_EMAIL', 3)
        self.max_attempts_per_cookie = getattr(settings, 'MAX_LOGIN_ATTEMPTS_COOKIE', 10)
        self.lockout_duration = getattr(settings, 'LOGIN_LOCKOUT_DURATION', 600)
        self.captcha_threshold = getattr(settings, 'LOGIN_CAPTCHA_THRESHOLD', 3)
        
        self.protected_urls = getattr(settings, 'LOGIN_SECURITY_URLS', [
            'login', 'api/login', 'auth/login', 'api/auth/login'
        ])
    
    def get_remaining_time_info(self, cache_key):
        try:
            if hasattr(cache, 'ttl'):
                ttl = cache.ttl(cache_key)
                if ttl and ttl > 0:
                    minutes = ttl // 60
                    seconds = ttl % 60
                    return {
                        'lock_time': f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s",
                        'total_seconds': ttl
                    }
        except (AttributeError, Exception):
            pass
        
        timestamp_key = f"{cache_key}_timestamp"
        duration_key = f"{cache_key}_duration"
        
        start_time = cache.get(timestamp_key)
        duration = cache.get(duration_key)
        
        if start_time and duration:
            elapsed = time.time() - start_time
            remaining = duration - elapsed
            
            if remaining > 0:
                minutes = int(remaining // 60)
                seconds = int(remaining % 60)
                return {
                    'lock_time': f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s",
                    'total_seconds': int(remaining)
                }
        
        return None
    
    def set_cache_with_ttl(self, key, value, duration):
        cache.set(key, value, duration)
        
        try:
            if not hasattr(cache, 'ttl'):
                timestamp_key = f"{key}_timestamp"
                duration_key = f"{key}_duration"
                cache.set(timestamp_key, time.time(), duration + 60)
                cache.set(duration_key, duration, duration + 60)
        except Exception:
            pass
    
    def process_request(self, request):
        if not self.should_check_request(request):
            return None
        
        client_id = self.get_or_create_client_id(request)
        email = self.extract_email(request)
        security_response = self.perform_security_checks(request, email, client_id)
        if security_response:
            return security_response

        request._security_email = email
        request._user_id = client_id
        
        return None
    
    def process_response(self, request, response):
        if not request.COOKIES.get(self.cookie_name):
            client_id = getattr(request, '_user_id', None)
            if not client_id:
                client_id = self.generate_client_id(request)
            
            response.set_cookie(
                self.cookie_name,
                client_id,
                max_age=self.cookie_max_age,
                httponly=True,
                secure=request.is_secure(),
                samesite='Lax'
            )
        if hasattr(request, '_security_email') and self.should_check_request(request):
            email = request._security_email
            client_id = getattr(request, '_user_id', '')
            
            if self.is_login_successful(response):
                self.handle_successful_login(email, client_id)
            elif response.status_code in [401, 403]:
                self.handle_failed_login(email, client_id, request)
        
        return response
    
    def should_check_request(self, request):
        if request.method != 'POST':
            return False
        
        try:
            url_name = resolve(request.path_info).url_name
            if url_name and any(protected in url_name for protected in self.protected_urls):
                return True
        except:
            pass
        
        path = request.path_info.strip('/')
        return any(protected in path for protected in self.protected_urls)
    
    def extract_email(self, request):
        email = None
        
        if hasattr(request, 'body') and request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                email = data.get('email')
            except:
                pass
            
        if not email and hasattr(request, 'POST'):
            email = request.POST.get('email')
        
        return email.lower().strip() if email else None
    
    def get_or_create_client_id(self, request):
        client_id = request.COOKIES.get(self.cookie_name)
        
        if not client_id or not self.is_valid_client_id(client_id):
            client_id = self.generate_client_id(request)
        
        return client_id
    
    def generate_client_id(self, request):
        unique_data = f"{uuid.uuid4()}-{request.META.get('HTTP_USER_AGENT', '')}-{time.time()}"
        return hashlib.sha256(unique_data.encode()).hexdigest()[:32]
    
    def is_valid_client_id(self, client_id):
        return client_id and len(client_id) == 32 and client_id.isalnum()
    
    def perform_security_checks(self, request, email, client_id):
        if self.is_globally_rate_limited():
            return ResponseHandler.json_rate_limited(
                message=ResponseMessages.TOO_MANY_REQUESTS,
            )
        
        if self.is_cookie_rate_limited(client_id):
            return ResponseHandler.json_rate_limited(
                message=ResponseMessages.TOO_MANY_REQUESTS,
            )
        
        if not email:
            return None

        plan_issue = self.check_company_plan_active(email)
        if plan_issue:
            return self.create_error_response(plan_issue, 403)
        
        if self.is_email_blocked(email):
            block_key = f'email_block_{email}'
            remaining_time = self.get_remaining_time_info(block_key)
            return ResponseHandler.json_rate_limited(
                message=ResponseMessages.TOO_MANY_REQUESTS,
                data={'remaining_time': remaining_time} if remaining_time else None
            )
        
        if self.is_captcha_required(email):
            captcha_response = self.extract_captcha(request)
            if not captcha_response or not self.verify_captcha(captcha_response):
                return ResponseHandler.json_rate_limited(
                    message=ResponseMessages.CAPTCHA_REQUIRED,
                )
        
        return None
    
    def is_globally_rate_limited(self):
        global_key = 'global_login_attempts'
        attempts = cache.get(global_key, 0)
        max_global = getattr(settings, 'MAX_GLOBAL_LOGIN_ATTEMPTS', 1000)
        
        if attempts >= max_global:
            return True
        
        self.set_cache_with_ttl(global_key, attempts + 1, 300)
        return False
    
    def is_cookie_rate_limited(self, client_id):
        cookie_key = f'login_attempts_cookie_{client_id}'
        attempts = cache.get(cookie_key, 0)
        
        if attempts >= self.max_attempts_per_cookie:
            return True
        
        return False
    
    def is_email_blocked(self, email):
        block_key = f'email_block_{email}'
        return cache.get(block_key, False)
    
    def is_captcha_required(self, email):
        captcha_key = f'captcha_required_{email}'
        return cache.get(captcha_key, False)
    
    def extract_captcha(self, request):
        if hasattr(request, 'body') and request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                return data.get('captcha_response')
            except:
                pass
        if hasattr(request, 'POST'):
            return request.POST.get('captcha_response')
        
        return None
    
    def verify_captcha(self, captcha_response):
        return True
    
    def is_login_successful(self, response):
        if response.status_code == 200:
            try:
                if hasattr(response, 'content'):
                    content = json.loads(response.content.decode('utf-8'))
                    return content.get('success', False) or 'token' in content
            except:
                pass
            return True
        return False
    
    def handle_successful_login(self, email, client_id):
        keys_to_clear = [
            f'failed_attempts_{email}',
            f'login_attempts_cookie_{client_id}',
            f'captcha_required_{email}',
            f'email_block_{email}',
        ]
        
        timestamp_keys = [f"{key}_timestamp" for key in keys_to_clear]
        duration_keys = [f"{key}_duration" for key in keys_to_clear]
        
        all_keys = keys_to_clear + timestamp_keys + duration_keys
        cache.delete_many(all_keys)
        
        logger.info(f"Successful login for email: {email} - All restrictions cleared")
    
    def handle_failed_login(self, email, client_id, request):
        failed_attempts_key = f'failed_attempts_{email}'
        failed_attempts = cache.get(failed_attempts_key, 0) + 1
        cookie_key = f'login_attempts_cookie_{client_id}'
        cookie_attempts = cache.get(cookie_key, 0) + 1
        self.set_cache_with_ttl(cookie_key, cookie_attempts, 3600)
        
        ip = self.get_client_ip(request)
        
        if failed_attempts >= self.max_attempts_per_email:
            block_key = f'email_block_{email}'
            self.set_cache_with_ttl(block_key, True, self.lockout_duration)
            cache.delete(failed_attempts_key)
            captcha_key = f'captcha_required_{email}'
            self.set_cache_with_ttl(captcha_key, True, 24 * 3600)
            
            logger.warning(
                f"EMAIL BLOCKED: {email} after {failed_attempts} consecutive failed attempts from IP: {ip}. "
                f"Blocked for {self.lockout_duration // 60} minutes."
            )
        else:
            self.set_cache_with_ttl(failed_attempts_key, failed_attempts, 3600)
            
            logger.warning(
                f"Failed login attempt #{failed_attempts} for email: {email} from IP: {ip}. "
                f"{self.max_attempts_per_email - failed_attempts} attempts remaining before block."
            )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def create_error_response(self, message, status_code, extra_data=None):
        current_time = datetime.now().isoformat()
        
        data = {
            'error': message,
            'success': False,
            'timestamp': current_time,
            'server_time': current_time
        }
        
        if extra_data:
            data.update(extra_data)
            
            if 'remaining_time' in extra_data and extra_data['remaining_time']:
                remaining_seconds = extra_data['remaining_time'].get('total_seconds', 0)
                if remaining_seconds > 0:
                    unblock_time = datetime.now() + timedelta(seconds=remaining_seconds)
                    data['unblock_time'] = unblock_time.isoformat()
                    data['unblock_time_formatted'] = unblock_time.strftime('%Y-%m-%d %H:%M:%S')
        
        response = JsonResponse(data, status=status_code)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response