from rest_framework import serializers
from shared.models.contract_management.employee_contract import EmployeeContract

class EmployeeContractSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    contract_type_name = serializers.ReadOnlyField(source='contract_type.contract_type_name')

    class Meta:
        model = EmployeeContract
        fields = '__all__'
        read_only_fields = ['company']

       
