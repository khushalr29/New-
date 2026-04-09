from rest_framework import serializers
from shared.models import AttendanceRegularization

class AttendanceRegularizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRegularization
        fields = [
            'id', 'employee', 'attendance_record', 
            'request_clock_in', 'request_clock_out', 'reason',
        ]

class AttendanceRegularizationListSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)

    class Meta:
        model = AttendanceRegularization
        fields = [
            'id', 'employee_name', 'attendance_record', 
            'request_clock_in', 'request_clock_out', 'reason',
            'created_at', 'updated_at',
        ]