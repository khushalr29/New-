from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

class CompanyEmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, company=None, **kwargs):
        if email is None or company is None:
            return None

        try:
            user = User.objects.get(email=email, company=company)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
