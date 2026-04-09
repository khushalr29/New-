from rest_framework import serializers
from shared.models.contract_management.contract_type import ContractType
from shared.utils.common.validation import validate_name

class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = '__all__'
        read_only_fields = ['company']

    def validate_name(self, value):
        return validate_name(value, field_name="Contract Type Name")

