from rest_framework import serializers
from shared.models.hr_management.hr_masters import DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = [
            'id',
            'document_type',
            'description',
            'status',
            'created_at',
            'updated_at',
            'deleted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']

class DocumentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'document_type', 'description', 'status', 'created_at', 'updated_at', 'deleted_at']