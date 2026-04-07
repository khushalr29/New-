from rest_framework import serializers
from shared.models import Role
from django.contrib.auth.models import Permission
from .permissionsSearializer import PermissionSerializer
from shared.utils.common import CaseInsensitiveUniqueTogetherValidator

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    company = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Role
        fields = ['name', 'permissions', 'company', 'is_enabled']

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['company'] = request.user.company

        validator = CaseInsensitiveUniqueTogetherValidator(
            model=Role,
            fields=['name', 'company']
        )
        validator(attrs, self)

        return super().validate(attrs)
    def create(self, validated_data):
        permission_codenames = validated_data.pop('permissions', [])

        group = Role.objects.create(**validated_data)
        permissions = Permission.objects.filter(codename__in=permission_codenames)
        group.permissions.set(permissions)
        return group

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','name','is_enabled']

class GroupDetailsSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)
    class Meta:
        model = Role
        fields = [
                  'id',
                  'name',
                  'permissions',
                  'is_enabled',
                ]

class GroupDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
                  'id',
                  'name'
                ]