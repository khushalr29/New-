from django.utils import translation
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from .jwt_auth import JWTAuthenticationMiddleware


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language_code = None
        
        # 1. Check if language is in JWT token
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                token = AccessToken(auth_header.split(' ')[1])
                language_code = token.get('language', None)
            except InvalidToken:
                pass
        
        # 2. Check if language is in request headers
        if not language_code:
            language_code = request.META.get('HTTP_ACCEPT_LANGUAGE')
            if language_code:
                language_code = language_code.split(',')[0].split('-')[0]
        
        # 3. Check if language is in query parameters
        if not language_code:
            language_code = request.GET.get('lang')
        
        # 4. Check user's preferred language from database
        if not language_code and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                from shared.models.core.user import User
                user = User.objects.get(id=request.user.id)
                language_code = getattr(user, 'preferred_language', None)
            except:
                pass
        
        # Validate and set language
        if language_code:
            supported_languages = [lang[0] for lang in settings.LANGUAGES]
            if language_code in supported_languages:
                translation.activate(language_code)
                request.LANGUAGE_CODE = language_code
            else:
                # Fallback to default language
                translation.activate(settings.LANGUAGE_CODE)
                request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        else:
            # Use browser's language or default
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        
        # Add language to response headers
        response = getattr(request, '_response', None)
        if response:
            response['Content-Language'] = request.LANGUAGE_CODE