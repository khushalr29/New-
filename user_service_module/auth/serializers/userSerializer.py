from shared.models import User, Employee
from django.conf import settings
from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from .permissionsSearializer import PermissionSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .groupSerializer import GroupDataSerializer, GroupDetailsSerializer
from shared.utils.common import CaseInsensitiveUniqueTogetherValidator, validate_email, validate_phone_number

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
            'id',
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
            'is_enabled',
            'status',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def get_permissions(self, obj):
        # Placeholder for custom permission logic if needed
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
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'email',
            'full_name',
            'country_number_code',
            'phone_number',
            'gender',
            'company',
            'account_type',
            'status',
            'is_enabled',
        ]

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            validate_email(self, email)

        if 'phone_number' in attrs and 'country_number_code' in attrs:
            attrs = validate_phone_number(
                attrs,
                phone_field='phone_number',
                code_field='country_number_code'
            )

        validator = CaseInsensitiveUniqueTogetherValidator(
            model=User,
            fields=['email', 'company']
        )
        validator(attrs, self)

        return attrs

    def update(self, instance, validated_data):
        image_url = validated_data.pop('image', None)
        instance = super().update(instance, validated_data)

        if image_url:
            instance.image = image_url
            instance.save()
            # Sync with Employee profile if exists
            employee = Employee.objects.filter(email=instance.email).first()
            if employee:
                employee.image = image_url
                employee.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    roles = GroupDetailsSerializer(many=True)
    sub_domain = serializers.SerializerMethodField()
    has_mpin = serializers.SerializerMethodField()
    company_plan_details = serializers.SerializerMethodField()
    joined = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'email',
            'full_name',
            'country_number_code',
            'phone_number',
            'gender',
            'account_type',
            'sub_domain',
            'company',
            'has_mpin',
            'user_permissions',
            'roles',
            'company_plan_details',
            'status',
            'joined',
            'is_enabled',
        ]

    def get_sub_domain(self, obj):
        if obj.company:
            return obj.company.sub_domain
        return None

    def get_has_mpin(self, obj):
        return obj.mpin is not None

    def get_company_plan_details(self, obj):
        company = obj.company
        if not company:
            return None

        return {
            "company_name": company.company_name,
            "company_code": company.company_code,
            "no_of_users": company.no_of_users,
            "no_of_employees": company.no_of_employees,
            "payment_status": company.payment_status,
            "amount_paid": float(company.amount_paid) if company.amount_paid is not None else 0.0,
        }

class UserListSerializer(serializers.ModelSerializer):
    roles = GroupDataSerializer(many=True)
    joined = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'image',
            'email',
            'full_name',
            'country_number_code',
            'phone_number',
            'gender',
            'roles',
            'status',
            'joined',
            'is_enabled',
            'company'
        ]

class UserDataSerializer(serializers.ModelSerializer):
    joined = serializers.DateTimeField(source='created_at', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'full_name','status','joined','is_enabled','company']