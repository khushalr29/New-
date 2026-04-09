from rest_framework import serializers
from shared.models import DocumentCategories

class DocumentCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategories
        fields = ['id', 'category_name', 'description','color', 'icon','mandatory_category','status']

class DocumentCategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategories
        fields = ['id', 'category_name', 'description','color', 'icon','mandatory_category','status','created_at','updated_at']