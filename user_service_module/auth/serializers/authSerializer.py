import re
from shared.models import User
from django.conf import settings
from django.utils.timezone import now
from django.core.mail import send_mail
from rest_framework import serializers
from shared.utils.response import ResponseMessages
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    company_id = serializers.IntegerField()
    host = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        company_id = attrs.get('company_id')
        host = attrs.get('host')
        cleaned_host = re.sub(r'^https?://', '', host).strip().lower()

        try:
            user = User.objects.get(email=email, company_id=company_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(ResponseMessages.USER_NOT_FOUND)

        company = user.company
        sub_domain = company.sub_domain or ''
        cleaned_sub_domain = re.sub(r'^https?://', '', sub_domain).strip().lower()

        if cleaned_host not in cleaned_sub_domain:
            raise AuthenticationFailed(ResponseMessages.SUBDOMAIN_ERROR)

        if not check_password(password, user.password):
            raise AuthenticationFailed(ResponseMessages.invalid_credentials())

        if not user.is_active:
            raise AuthenticationFailed(ResponseMessages.user_account_disabled())

        attrs['user'] = user
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    host = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['email', 'host']
  
    def validate(self, attrs):
        email = attrs.get('email')
        host = attrs.get('host')

        cleaned_host = re.sub(r'^https?://', '', host).strip().lower()

        try:
            # We filter by company domain to ensure we get the correct user if same email exists in multiple companies
            user = User.objects.filter(
                email=email, 
                company__sub_domain__icontains=cleaned_host
            ).first()
            if not user:
                 raise serializers.ValidationError(ResponseMessages.NOT_REGISTERED_USER)
        except User.DoesNotExist:
            raise serializers.ValidationError(ResponseMessages.NOT_REGISTERED_USER)
        
        company = user.company
        sub_domain = company.sub_domain or ''
        cleaned_sub_domain = re.sub(r'^https?://', '', sub_domain).strip().lower()

        if cleaned_host not in cleaned_sub_domain:
            raise serializers.ValidationError(ResponseMessages.SUBDOMAIN_ERROR)

        uid = urlsafe_base64_encode(force_bytes(user.email))
        token = PasswordResetTokenGenerator().make_token(user)
        link = f'{sub_domain}/reset-password?userId={uid}&token={token}'
        
        message = render_to_string('email_templates/password_reset_template.html', {
            'user': user.full_name,
            'set_link': link,
        })
        subject = "Reset your password"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=message,
        )
        
        return attrs

class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != confirm_password:
                raise serializers.ValidationError(ResponseMessages.PASSWORD_MISMATCH)
            email = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(email=email)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(ResponseMessages.INVALID_TOKEN)
            user.set_password(password)
            user.auth_token_issued_at = now()
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError(ResponseMessages.INVALID_TOKEN)
        
class SetMPinSerializer(serializers.Serializer):
    mpin = serializers.CharField(min_length=6, max_length=6, write_only=True)

    def validate_mpin(self, value, field_name='MPIN'):
        if not value.isdigit():
            raise serializers.ValidationError(ResponseMessages.INVALID_MPIN.format(field_name=field_name))
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        mpin = attrs.get('mpin')

        if len(str(mpin)) != 6:
            raise serializers.ValidationError(ResponseMessages.MPIN_LENGTH_ERROR)

        user.mpin = mpin
        user.save(update_fields=['mpin'])
        return attrs

class CheckMPinSerializer(serializers.Serializer):
    mpin = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        mpin = attrs.get('mpin')

        if not user.mpin:
            raise serializers.ValidationError(ResponseMessages.MPIN_NOT_SET)

        if str(user.mpin) != str(mpin):
            raise serializers.ValidationError(ResponseMessages.MPIN_INPUT_DOES_NOT_MATCH_SET)

        return attrs
    
class VerifyPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        user = self.context['request'].user
        password = attrs.get('password')

        if not check_password(password, user.password):
            raise serializers.ValidationError({'password': ResponseMessages.invalid_credentials()})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.mpin = None
        user.save(update_fields=['mpin'])
        return user