from django.db import models
from ..core.employee import Employee
from .leave_type import LeaveType
from ..core.base import TenantModel

class LeaveApplication(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_applications')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'leave_application'

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.leave_type_name}" 