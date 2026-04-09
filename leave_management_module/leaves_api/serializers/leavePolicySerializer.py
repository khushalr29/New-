from rest_framework import serializers
from shared.models.leave_management.leave_policies import LeavePolicy

class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicy
        fields = '__all__'
        read_only_fields = ['company']