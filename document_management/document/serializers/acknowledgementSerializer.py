from rest_framework import serializers
from shared.models import Acknowledgement

class AcknowledgementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acknowledgement
        fields = ['id', 'document', 'user', 'due_date', 'note']

class AcknowledgementListSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.document_title', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = Acknowledgement
        fields = ['id', 'document', 'document_title', 'user', 'user_name', 'due_date', 'note','created_at','updated_at']