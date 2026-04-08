from rest_framework import serializers
from shared.models import AttendancePolicy

class AttendencePolicySerializer(serializers.ModelSerializer):
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
        ]

    def validate(self, attrs):
        late = attrs.get('late_arrival_grace_time')
        early = attrs.get('early_departure_grace_time')
        if late is not None and early is not None:
            if late < early:
                raise serializers.ValidationError("Early departure grace time cannot be greater than late arrival grace time")
        return attrs

class AttendencePolicyListSerializer(serializers.ModelSerializer):
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
            'created_at',
            'updated_at',
        ]
