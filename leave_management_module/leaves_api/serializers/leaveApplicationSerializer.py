from rest_framework import serializers
from shared.models.leave_management.leave_application import LeaveApplication

class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = '__all__'
        read_only_fields = ['company']