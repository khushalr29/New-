import jwt
from ..models import User
from django.conf import settings
from django.utils.timezone import now
from ..utils.response import ResponseHandler
from ..utils.response import ResponseMessages
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    ALLOWED_PATHS_FOR_NO_AUTH = [
        '/admin/',
        '/swagger/',
        '/api/v1/auth/enums',
        '/api/v1/auth/logins',
        '/api/v1/auth/check-domains',
        '/api/v1/auth/send-reset-password-emails',
        '/api/v1/auth/setpassword',
        '/api/v1/auth/refreshtokens',
        '/api/v1/auth/login/',
    ]

    ALLOWED_PATHS_ON_COMPANY_SUBSCRIPTION_END = [
        '/api/v1/auth/logouts',
    ]
    def process_request(self, request):
        path = str(request.path)

        if any(path.startswith(p) for p in self.ALLOWED_PATHS_FOR_NO_AUTH):
            return None

        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return ResponseHandler.json_unauthorized(message=ResponseMessages.AUTH_HEADER_MISSING_OR_INVALID)

        token = auth_header.split(' ')[1]

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.INVALID_TOKEN)

        sub = decoded.get('sub', '')
        try:
            user_id, company_id, impersonation_flag = sub.split('-')
            user_id = int(user_id)
            company_id = int(company_id)
            impersonation_flag = impersonation_flag.lower()
        except ValueError:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.INVALID_TOKEN_SUBJECT)

        try:
            user = User.objects.select_related('company').get(
                id=user_id,
                company_id=company_id,
                account_type__in=[
                    User.SUPER_ADMIN,
                    User.SUB_ADMIN,
                    User.COMPANY_SUPER_ADMIN,
                    User.COMPANY_SUB_ADMIN,
                ]
            )
        except User.DoesNotExist:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.USER_NOT_FOUND)
        
        company = user.company
        if not company:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.COMPANY_NOT_FOUND)
        
        token_iat = decoded.get('iat')
        if token_iat is None:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.TOKEN_MISSING_IAT)

        if not hasattr(user, 'auth_token_issued_at') or user.auth_token_issued_at is None:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.USER_TOKEN_ISSUED_AT_MISSING)

        if int(user.auth_token_issued_at.timestamp()) != token_iat:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.SESSION_EXPIRED)

        if company.subscription_end_date and company.subscription_end_date < now().date():
            if any(path.startswith(p) for p in self.ALLOWED_PATHS_ON_COMPANY_SUBSCRIPTION_END):
                if not (user.is_superuser or user.account_type == User.COMPANY_SUPER_ADMIN):
                    return ResponseHandler.json_forbidden(message=ResponseMessages.COMPANY_SUBSCRIPTION_EXPIRED_CONTACT_ADMIN)
            else:
                return ResponseHandler.json_forbidden(message=ResponseMessages.COMPANY_SUBSCRIPTION_EXPIRED)

        if not user.is_active:
            return ResponseHandler.json_unauthorized(message=ResponseMessages.ACCOUNT_SUSPENDED)

        request.user = user
        request.is_superuser_or_impersonation = (
            user.is_superuser or impersonation_flag == 'true' or user.account_type == User.COMPANY_SUPER_ADMIN
        )

        return None
 