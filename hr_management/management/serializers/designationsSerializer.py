from rest_framework import serializers
from shared.models.hr_management.hr_masters import Designation

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'title','designation', 'department', 'status', 'created_at', 'updated_at', 'deleted_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

class DesignationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'title','designation', 'department','status', 'created_at', 'updated_at', 'deleted_at']