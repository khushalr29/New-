from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    """
    Stand-alone professional login to obtain JWT tokens for the Meeting Service.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Please provide both email and password."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using the custom shared User model
        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {email} successfully logged into the Meeting Service.")
            return Response({
                'success': True,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'email': user.email,
                    'full_name': getattr(user, 'full_name', 'User'),
                    'company': user.company.company_name if user.company else None
                }
            }, status=status.HTTP_200_OK)
        
        logger.warning(f"Failed login attempt for email: {email}")
        return Response({"error": "Invalid credentials. Please try again."}, status=status.HTTP_401_UNAUTHORIZED)
