from rest_framework import serializers
from shared.models import Attendance

class AttendenceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'date', 'clock_in', 'clock_out', 
            'shift', 'status', 'late_by', 'overtime', 
            'total_work_hours', 'is_overtime', 'is_holiday', 'remarks',
        ]

class AttendenceRecordListSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    shift_name = serializers.CharField(source='shift.shift_name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee_name', 'date', 'clock_in', 'clock_out', 
            'shift_name', 'status', 'late_by', 'overtime', 
            'total_work_hours', 'is_overtime', 'is_holiday', 'remarks',
            'created_at', 'updated_at',
        ]