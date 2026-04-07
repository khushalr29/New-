from shared.models import User
from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
              'id',
              'codename',
              'name',
              'content_type'
            ]

class UserPermissionsSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'user_permissions']