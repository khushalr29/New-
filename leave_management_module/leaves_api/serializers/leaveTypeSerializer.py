from rest_framework import serializers
from shared.models.leave_management.leave_type import LeaveType

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
        read_only_fields = ['company']