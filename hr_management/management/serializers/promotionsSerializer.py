from rest_framework import serializers
from shared.models.hr_management import Promotion
from .employeeSerializer import EmployeeSerializer
from .designationsSerializer import DesignationSerializer

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            'id',
            'employee',
            'promotion_title',
            'description',
            'promotion_date',
            'old_designation',
            'new_designation',
            'salary_adjustment',
            'reason_for_promotion',
            'document',
            'status'
        ]

class PromotionListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    old_designation = DesignationSerializer(read_only=True)
    new_designation = DesignationSerializer(read_only=True)
    class Meta:
        model = Promotion
        fields = [
            'id',
            'employee',
            'promotion_title',
            'description',
            'promotion_date',
            'old_designation',
            'new_designation',
            'salary_adjustment',
            'reason_for_promotion',
            'document',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]