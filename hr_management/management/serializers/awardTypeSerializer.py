from rest_framework import serializers
from shared.models.hr_management.hr_masters import AwardType

class AwardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardType
        fields = [
            'id',
            'award_type',
            'description',
            'status'
        ]

class AwardTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardType
        fields = [
            'id',
            'award_type',
            'description',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]