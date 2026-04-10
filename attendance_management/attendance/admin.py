from django.contrib import admin
from shared.models.attendance import Shift, AttendancePolicy, Attendance, AttendanceRegularization

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_name', 'start_time', 'end_time', 'break_duration', 'grade_period', 'is_night_shift', 'status', 'created_at')
    list_filter = ('is_night_shift', 'status')
    search_fields = ('shift_name',)
    ordering = ('shift_name',)
    
@admin.register(AttendancePolicy)
class AttendancePolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'description', 'late_arrival_grace_time', 'early_departure_grace_time', 'overtime_rate_per_hour', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('policy_name', 'description')
    ordering = ('policy_name',)
    
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'clock_in', 'clock_out', 'status', 'created_at')
    list_filter = ('date', 'status', 'shift')
    search_fields = ('employee__full_name',)
    ordering = ('-date', 'employee')
    
@admin.register(AttendanceRegularization)
class AttendanceRegularizationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'attendance_record', 'request_clock_in', 'request_clock_out', 'reason', 'created_at')
    list_filter = ('employee', 'attendance_record__date')
    search_fields = ('employee__full_name', 'reason')
    ordering = ('-created_at',)