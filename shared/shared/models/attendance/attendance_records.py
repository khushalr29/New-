from django.db import models
from ..core.base import TenantModel
from ..core.employee import Employee
from .attendance_shift import Shift
from ..core.enums import CommonStatus, AttendanceStatus
from .attendance_policy import AttendancePolicy

class Attendance(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendances')
    status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    late_by = models.DurationField(null=True, blank=True)
    overtime = models.DurationField(null=True, blank=True)
    total_work_hours = models.DurationField(null=True, blank=True)
    is_overtime = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    is_holiday = models.BooleanField(default=False)

    class Meta:
        db_table = 'attendance'
        unique_together = ('employee', 'date', 'company')
        ordering = ['-date', 'employee']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.status})"
