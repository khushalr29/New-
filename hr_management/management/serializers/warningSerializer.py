from rest_framework import serializers
from shared.models.hr_management import Warning
from ..serializers.employeeSerializer import EmployeeSerializer

class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = [
            'id',
            'warning_by',
            'warning_to',
            'warning_type',
            'subject',
            'severity',
            'warning_date',
            'description',
            'document',
            'expiry_date',
            'has_improvement_plan',
            'improvement_plan_goal',
            'improvement_plan_start_date',
            'improvement_plan_end_date',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

class WarningListSerializer(serializers.ModelSerializer):
    warning_by = EmployeeSerializer(read_only=True)
    warning_to = EmployeeSerializer(read_only=True)
    class Meta:
        model = Warning
        fields = [
            'id',
            'warning_by',
            'warning_to',
            'warning_type',
            'subject',
            'severity',
            'warning_date',
            'description',
            'document',
            'expiry_date',
            'has_improvement_plan',
            'improvement_plan_goal',
            'improvement_plan_start_date',
            'improvement_plan_end_date',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]