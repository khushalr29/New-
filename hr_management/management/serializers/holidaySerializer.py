from rest_framework import serializers
from shared.models.hr_management.hr_masters import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields= [
            'id',
            'holiday_name',
            'category',
            'start_date',
            'end_date',
            'description',
            'is_paid_holiday',
            'is_half_day',
            'applicable_branches',
            'status'
        ]

class HolidayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields= [
            'id',
            'holiday_name',
            'category',
            'start_date',
            'end_date',
            'description',
            'is_paid_holiday',
            'is_half_day',
            'applicable_branches',
            'status',
            'company',
            'created_at',
            'updated_at',
            'deleted_at'
        ]