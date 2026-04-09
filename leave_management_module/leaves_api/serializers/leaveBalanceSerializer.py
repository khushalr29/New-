from rest_framework import serializers
from shared.models.leave_management.leave_balances import LeaveBalance

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ['company']