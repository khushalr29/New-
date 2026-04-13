from rest_framework import serializer
from shared.models.hr_management.award import Award
from .awardTypeListSerializer import AwardTypeSerializer

class AwardSerializer(serializer.ModelSerializer):
    class Meta:
        model = Award
        fields = [
            'id',
            'employee',
            'award_type',
            'date_awarded',
            'gift',
            'description',
            'certificate',
            'photo'
        ]

class AwardListSerializer(serializer.ModelSerializer):
    award_type = AwardTypeSerializer(read_only=True)
    class Meta:
        model = Award
        fields = [
            'id',
            'employee',
            'award_type',
            'date_awarded',
            'gift',
            'description',
            'certificate',
            'photo',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
            ]