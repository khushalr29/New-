from rest_framework import serializers
from shared.models.core.employee import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'employee_id',
            'employee_code',
            'email',
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
            'user',
            'manager',
            'identity_type',
            'identity_number',
            'address',
            'country_number_code',
            'phone',
            'status',
        ]

class EmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'full_name',
            'employee_id',
            'employee_code',
            'email',
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
            'user',
            'manager',
            'identity_type',
            'identity_number',
            'address',
            'country_number_code',
            'phone',
            'status',
        ]