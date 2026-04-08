from django.db import models
from ..core.base import TenantModel
from ..core.employee import Employee
from .attendence_records import Attendance

class AttendanceRegularization(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_regularizations')
    attendance_record = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='attendance_regularizations')
    request_clock_in = models.TimeField(null=True, blank=True)
    request_clock_out = models.TimeField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'attendance_regularization'

    def __str__(self):
        return f"Regularization for {self.employee.full_name} - {self.attendance_record.date}"