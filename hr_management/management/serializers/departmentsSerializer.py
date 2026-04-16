from rest_framework import serializers
from shared.models.hr_management.hr_masters import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'branch',
            'department',
            'description',
            'unique_code',
            'parent',
            'status',
            'created_by',
        ]

class DepartmentListSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.branch_name', read_only=True)

    class Meta:
        model = Department
        fields = [
            'id',
            'branch',
            'branch_name',
            'department',
            'description',
            'unique_code',
            'parent',
            'status',
            'created_by',
            'created_at',
            'updated_at',
            'deleted_at',
        ]