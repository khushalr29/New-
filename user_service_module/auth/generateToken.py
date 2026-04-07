from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now

def get_tokens_for_user(user):
    user.auth_token_issued_at = now()
    user.save(update_fields=['auth_token_issued_at'])

    refresh = RefreshToken.for_user(user)

    iat_timestamp = int(user.auth_token_issued_at.timestamp())
    refresh['iat'] = iat_timestamp
    access = refresh.access_token
    access['iat'] = iat_timestamp
    
    sub = f"{user.id}-{user.company.id if user.company else 0}-{'true' if user.is_superuser else 'false'}"
    refresh['sub'] = sub
    access['sub'] = sub
    
    refresh['impersonation'] = False
    access['impersonation'] = False

    return {
        'refresh': str(refresh),
        'access': str(access),
    }

def generate_impersonation_tokens(user):
    issued_at = user.auth_token_issued_at or now()
    iat_timestamp = int(issued_at.timestamp())

    refresh = RefreshToken.for_user(user)
    refresh['iat'] = iat_timestamp

    access = refresh.access_token
    access['iat'] = iat_timestamp

    sub = f"{user.id}-{user.company.id if user.company else 0}-true"
    refresh['sub'] = sub
    access['sub'] = sub

    refresh['impersonation'] = True
    access['impersonation'] = True

    return {
        'refresh': str(refresh),
        'access': str(access),
    }