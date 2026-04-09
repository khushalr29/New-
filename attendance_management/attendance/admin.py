from django.contrib import admin
from shared.models.attendence import Shift, AttendencePolicy, AttendenceRecords, AttendenceRegularization

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'description', 'effective_from', 'effective_to', 'grace_period', 'late_mark_threshold', 'early_leave_threshold', 'half_day_threshold', 'full_day_threshold', 'status', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('policy_name', 'description', 'effective_from', 'effective_to', 'grace_period', 'late_mark_threshold', 'early_leave_threshold', 'half_day_threshold', 'full_day_threshold', 'status', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('policy_name', 'description', 'effective_from', 'effective_to', 'grace_period', 'late_mark_threshold', 'early_leave_threshold', 'half_day_threshold', 'full_day_threshold', 'status', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('policy_name', 'description', 'effective_from', 'effective_to', 'grace_period', 'late_mark_threshold', 'early_leave_threshold', 'half_day_threshold', 'full_day_threshold', 'status', 'created_at', 'updated_at', 'deleted_at')
    
@admin.register(AttendencePolicy)
class AttendencePolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_name', 'description', 'late_arrival_grace_time', 'early_departure_grace_time', 'overtime_rate_per_hour', 'status', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('policy_name', 'description', 'late_arrival_grace_time', 'early_departure_grace_time', 'overtime_rate_per_hour', 'status', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('policy_name', 'description', 'late_arrival_grace_time', 'early_departure_grace_time', 'overtime_rate_per_hour', 'status', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('policy_name', 'description', 'late_arrival_grace_time', 'early_departure_grace_time', 'overtime_rate_per_hour', 'status', 'created_at', 'updated_at', 'deleted_at')
    
@admin.register(AttendenceRecords)
class AttendenceRecordsAdmin(admin.ModelAdmin):
    list_display = ('employee', 'check_in', 'check_out', 'status', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('employee', 'check_in', 'check_out', 'status', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('employee', 'check_in', 'check_out', 'status', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('employee', 'check_in', 'check_out', 'status', 'created_at', 'updated_at', 'deleted_at')
    
@admin.register(AttendenceRegularization)
class AttendenceRegularizationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'reason', 'status', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('employee', 'date', 'reason', 'status', 'created_at', 'updated_at', 'deleted_at')
    search_fields = ('employee', 'date', 'reason', 'status', 'created_at', 'updated_at', 'deleted_at')
    ordering = ('employee', 'date', 'reason', 'status', 'created_at', 'updated_at', 'deleted_at')
    