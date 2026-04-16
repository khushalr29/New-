class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')
        request.platform = request.META.get('HTTP_X_PLATFORM', 'web')
        request.app_version = request.META.get('HTTP_X_VERSION', '1.0.0')
        request.timezone = request.META.get('HTTP_X_TIMEZONE', '0')
        
        response = self.get_response(request)
        return response