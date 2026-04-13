from rest_framework import serializers
from shared.models import AttendancePolicy, Shift

class AttendancePolicyListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = AttendancePolicy
        fields = [
            'id',
            'policy_name',
            'description',
            'late_arrival_grace_time',
            'early_departure_grace_time',
            'overtime_rate_per_hour',
            'status',
            'company_name',
        ]

class ShiftListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'shift_name', 'start_time', 'end_time', 'status']