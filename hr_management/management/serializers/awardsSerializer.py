from rest_framework import serializers
from shared.models.hr_management.award import Award
from .awardTypeSerializer import AwardTypeSerializer
from .employeeSerializer import EmployeeSerializer

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = [
            'id',
            'employee',
            'award_type',
            'date_awarded',
            'gift',
            'description',
            'certificate',
            'photo'
        ]

class AwardListSerializer(serializers.ModelSerializer):
    award_type = AwardTypeSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Award
        fields = [
            'id',
            'employee',
            'award_type',
            'date_awarded',
            'gift',
            'description',
            'certificate',
            'photo',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
            ]