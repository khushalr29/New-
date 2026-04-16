from rest_framework import serializers
from shared.models import Employee, EmployeeDocument
from django.db import transaction
from .branchSerializer import BranchSerializer
from .departmentsSerializer import DepartmentSerializer
from .designationsSerializer import DesignationSerializer
from shared.serializers.commonSerializer import ShiftListSerializer as ShiftSerializer, AttendancePolicyListSerializer as AttendencePolicySerializer
class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = [
            'id',
            'employee',
            'document_type',
            'document_file',
        ]

class EmployeeDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = [
            'id',
            'employee',
            'document_type',
            'document_file',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Employee
        fields = [
            'id',
            'full_name',
            'employee_id',
            'employee_code',
            'official_email_id',
            'profile_image',
            'branch',
            'department',
            'designation',
            'shift',
            'user_id',
            'manager',
            'country_number_code',
            'phone_number',
            'status',
            'created_by',
            'updated_by',
            'deleted_by'
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    department = DepartmentSerializer()
    designation = DesignationSerializer()
    shift = ShiftSerializer()
    attendence_policy = AttendencePolicySerializer()
    manager = ManagerSerializer()
    employee_documents = EmployeeDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'employee_id',
            'employee_code',
            'personal_email_id',
            'official_email_id',
            'password',
            'date_of_birth',
            'profile_image',
            'gender',
            'branch',
            'department',
            'designation',
            'date_of_joining',
            'employment_type',
            'shift',
            'attendence_policy',
            'user_id',
            'manager',
            'identity_type',
            'identity_number',
            'address',
            'country_number_code',
            'phone_number',
            'status',
            'bank_name',
            'account_holder_name',
            'bank_account_number',
            'bank_ifsc_code',
            'bank_branch_name',
            'tax_payer_id',
            'base_salary',
            'emergency_contact_name',
            'emergency_contact_number',
            'emergency_contact_relationship',
            'resume',
            'employee_documents',
            'created_by',
            'updated_by',
            'deleted_by'
        ]
    def create(self, validated_data):
        employee_documents = validated_data.pop('employee_documents')
        with transaction.atomic():
            employee = Employee.objects.create(**validated_data)
            for employee_document in employee_documents:
                EmployeeDocument.objects.create(employee=employee, **employee_document)
        return employee

    def update(self, instance, validated_data):
        employee_documents = validated_data.pop('employee_documents')
        with transaction.atomic():
            employee = super().update(instance, validated_data)
            for employee_document in employee_documents:
                EmployeeDocument.objects.create(employee=employee, **employee_document)
        return employee

class EmployeeListSerializer(serializers.ModelSerializer):
    employee_documents = EmployeeDocumentListSerializer(many=True, read_only=True)
    branch = BranchSerializer()
    department = DepartmentSerializer()
    designation = DesignationSerializer()
    shift = ShiftSerializer()
    attendence_policy = AttendencePolicySerializer()
    manager = ManagerSerializer()
    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'employee_id',
            'employee_code',
            'personal_email_id',
            'official_email_id',
            'date_of_birth',
            'profile_image',
            'gender',
            'branch',
            'department',
            'designation',
            'date_of_joining',
            'employment_type',
            'shift',
            'attendence_policy',
            'user_id',
            'manager',
            'identity_type',
            'identity_number',
            'employee_permissions',
            'address',
            'country_number_code',
            'phone_number',
            'status',
            'bank_name',
            'account_holder_name',
            'bank_account_number',
            'bank_ifsc_code',
            'bank_branch_name',
            'tax_payer_id',
            'base_salary',
            'emergency_contact_name',
            'emergency_contact_number',
            'emergency_contact_relationship',
            'resume',
            'employee_documents',
            'created_by',
            'updated_by',
            'deleted_by',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']