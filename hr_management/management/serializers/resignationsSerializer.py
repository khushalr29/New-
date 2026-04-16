from rest_framework import serializers
from shared.models.hr_management import Resignations
from management.serializers.employeeSerializer import EmployeeSerializer

class ResignationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resignations
        fields = [
            'id',
            'employee',
            'resignation_date',
            'last_working_day',
            'notice_period',
            'resignation_reason',
            'description',
            'document',
            'status'
        ]

class ResignationsListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Resignations
        fields = [
            'id',
            'employee',
            'resignation_date',
            'last_working_day',
            'notice_period',
            'resignation_reason',
            'description',
            'document',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]

