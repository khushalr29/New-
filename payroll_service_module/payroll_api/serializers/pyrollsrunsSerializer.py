from rest_framework import serializers
from shared.models.payroll_management.payrollRuns import PayrollRun

class PayrollRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollRun
        fields = '__all__'