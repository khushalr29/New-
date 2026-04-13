from rest_framework import serializers
from shared.models.hr_management import Termination

class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        fields = [
            'id',
            'employee',
            'termination_date',
            'termination_type',
            'termination_reason',
            'description',
            'document',
            'status'
        ]

class TerminationListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Termination
        fields = [
            'id',
            'employee',
            'termination_date',
            'termination_type',
            'termination_reason',
            'description',
            'document',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
