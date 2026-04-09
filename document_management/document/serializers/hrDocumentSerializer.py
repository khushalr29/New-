from rest_framework import serializers
from shared.models import HRDocument

class HRDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HRDocument
        fields = ['id', 'document_title', 'description','category','file','effective_date','expiry_date','is_requires_acknowledgement']

class HRDocumentListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    class Meta:
        model = HRDocument
        fields = ['id', 'document_title', 'description','category','category_name','file','effective_date','expiry_date','is_requires_acknowledgement','created_at','updated_at']
