from rest_framework import serializer
from shared.models.hr_management.hr_masters import Holiday

class HolidaySerializer(serializer.ModelSerializer):
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

class HolidayListSerializer(serializer.ModelSerializer):
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