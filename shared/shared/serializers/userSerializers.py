from shared.models import User
from django.conf import settings
from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from shared.utils.common import CaseInsensitiveUniqueTogetherValidator, validate_phone_number

class UserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    permissions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'image',
            'full_name',
            'email',
            'country_number_code',
            'phone_number',
            'gender',
            'company',
            'permissions',
            'account_type',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def get_permissions(self, obj):
        return []

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })

        phone_number = attrs.get('phone_number')
        country_code = attrs.get('country_number_code')
        if phone_number and country_code:
            phone_validated = validate_phone_number(
                {'phone_number': phone_number, 'country_number_code': country_code},
                phone_field='phone_number',
                code_field='country_number_code'
            )
            attrs['phone_number'] = phone_validated['phone_number']

        validator = CaseInsensitiveUniqueTogetherValidator(
            model=User,
            fields=['email', 'company']
        )
        validator(attrs, self)

        return super().validate(attrs)

    def send_create_password_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.email))
        token = PasswordResetTokenGenerator().make_token(user)
        base_url = user.company.sub_domain if user.company else settings.FRONTEND_URL
        link = f'{base_url}/reset-password?userId={uid}&token={token}'

        message = render_to_string('email_templates/password_set_template.html', {
            'user': user.full_name,
            'set_link': link,
        })
        subject = "Set your password"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=message,
        )

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user