from rest_framework import serializers
from shared.models import Document

class DocumentTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'template_name', 'category', 'file_format', 'status','description','is_set_default_category','content','placeholder','default_values']

class DocumentTemplatesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'template_name', 'category', 'file_format', 'status','description','is_set_default_category','content','placeholder','default_values','created_at','updated_at']