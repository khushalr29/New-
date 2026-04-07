from shared.models import User
from ..renders import UserRenderer
from shared.models import Company
from django.utils.timezone import now
from rest_framework.views import APIView
from shared.models import UserActivityLog
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from shared.utils.response import ResponseHandler,ResponseMessages
from ..generateToken import generate_impersonation_tokens, get_tokens_for_user
from ..serializers.authSerializer import (SetPasswordSerializer,UserLoginSerializer,SendPasswordResetEmailSerializer,
                                          CheckMPinSerializer,SetMPinSerializer,VerifyPasswordSerializer)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            token = get_tokens_for_user(user)
            UserActivityLog.objects.create(user=user, action=UserActivityLog.LOGIN)

            return ResponseHandler.success(
                response_data={
                    'access': token['access'],
                    'refresh': token['refresh']
                },message=ResponseMessages.LOGIN_SUCCESS
            )
        return ResponseHandler.bad_request(response_data=serializer.errors, message=ResponseMessages.VALIDATION_ERROR)

class ImpersonationLoginView(APIView):
    def post(self, request):
        company_id = request.data.get('Company_id')
        if not company_id:
            return ResponseHandler.bad_request(message=ResponseMessages.TARGET_ID_ERROR)

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.COMPANY_NOT_FOUND)

        if request.user.account_type != User.SUPER_ADMIN:
            return ResponseHandler.forbidden(message=ResponseMessages.IMPERSONATION_NOT_ALLOWED)

        try:
            target_user = User.objects.get(
                company=company,
                account_type=User.COMPANY_SUPER_ADMIN
            )
        except User.DoesNotExist:
            return ResponseHandler.not_found(message=ResponseMessages.TARGET_USER_ERROR)

        tokens = generate_impersonation_tokens(target_user)
        redirect_url = company.sub_domain

        return Response({
            "message": "Impersonation successful.",
            "redirect_to": redirect_url,
            "token": tokens['access'],
            "user": target_user.id,
            "company_id": company.id
        }, status=200)

class UserLogoutView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            user.auth_token_issued_at = now()
            user.save(update_fields=['auth_token_issued_at'])

            UserActivityLog.objects.create(user=user, action=UserActivityLog.LOGOUT)
            return ResponseHandler.success(message=ResponseMessages.LOGOUT_SUCCESS)
        return ResponseHandler.unauthorized()

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ResponseHandler.success(message=ResponseMessages.PASSWORD_EMAIL_SENT)

class SetPasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request, uid, token, format=None):
        serializer = SetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return ResponseHandler.success(message=ResponseMessages.PASSWORD_UPDATED)

class CheckDomainExistenceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_domain = request.query_params.get('domain')

        if not user_domain:
            return ResponseHandler.warn({"exists": False})

        if not user_domain.startswith(('https://')):
            cleaned_user_domain = f'https://{user_domain}'
        else:
            cleaned_user_domain = user_domain

        company = Company.objects.filter(sub_domain=cleaned_user_domain).first()
        if company:
            return ResponseHandler.success({"exists": True, "company_id": company.id})
        else:
            return ResponseHandler.success({"exists": False})

class SetMPinView(APIView):
    def patch(self, request):
        serializer = SetMPinSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return ResponseHandler.success(message=ResponseMessages.MPIN_UPDATED)
    
class CheckMPinView(APIView):
    def post(self, request):
        serializer = CheckMPinSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return ResponseHandler.success(message=ResponseMessages.MPIN_VERIFIED)
    
class VerifyPasswordView(APIView):
    def post(self, request):
        serializer = VerifyPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return ResponseHandler.success(message=ResponseMessages.PASSWORD_VERIFIED)