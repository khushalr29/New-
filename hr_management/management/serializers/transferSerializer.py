from rest_framework import serializers
from shared.models.hr_management import Transfer
from ..serializers.employeeSerializer import EmployeeSerializer
from ..serializers.branchSerializer import BranchSerializer
from ..serializers.departmentsSerializer import DepartmentSerializer

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            'id',
            'employee',
            'transfer_title',
            'description',
            'transfer_date',
            'old_department',
            'new_department',
            'old_branch',
            'new_branch',
        ]

class TransferListSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    old_department = DepartmentSerializer(read_only=True)
    new_department = DepartmentSerializer(read_only=True)
    old_branch = BranchSerializer(read_only=True)
    new_branch = BranchSerializer(read_only=True)
    class Meta:
        model = Transfer
        fields = [
            'id',
            'employee',
            'transfer_title',
            'description',
            'transfer_date',
            'old_department',
            'new_department',
            'old_branch',
            'new_branch',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]