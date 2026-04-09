from rest_framework import serializers
from shared.models.contract_management.contract_template import ContractTemplate

class ContractTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractTemplate
        fields = '__all__'
        read_only_fields = ['company']