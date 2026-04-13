from rest_framework import serializers
from shared.models.hr_management import Resignation

class ResignationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Resignation
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

class ResignationListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Resignation
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

