from rest_framework import serializers
from shared.models import Shift

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = [
            'id', 'shift_name', 'start_time', 'end_time', 
            'break_duration', 'break_start_time', 'break_end_time', 
            'grade_period', 'is_night_shift', 'status'
        ]
        read_only_fields = ['id']

class ShiftListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'shift_name', 'start_time', 'end_time', 'status']