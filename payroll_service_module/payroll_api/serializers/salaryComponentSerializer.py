from rest_framework import serializers
from shared.models.payroll_management.salaryComponents import SalaryComponent

class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = '__all__'
