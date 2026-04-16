from rest_framework import serializers
from shared.models.hr_management import Termination
from .employeeSerializer import EmployeeSerializer

class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        fields = [
            'id',
            'employee',
            'termination_type',
            'termination_date',
            'last_working_day',
            'termination_reason',
            'description',
            'document',
            'status',
            'exit_interview_conducted',
            'exit_interview_date',
            'exit_feedback'
        ]

class TerminationListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Termination
        fields = [
            'id',
            'employee',
            'termination_type',
            'termination_date',
            'last_working_day',
            'termination_reason',
            'description',
            'document',
            'status',
            'exit_interview_conducted',
            'exit_interview_date',
            'exit_feedback',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
