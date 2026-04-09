from django.db import models
from ..core.employee import Employee
from .leave_type import LeaveType
from ..core.base import TenantModel

class LeaveStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'
    CANCELLED = 'cancelled', 'Cancelled'

class LeaveApplication(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_applications')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=LeaveStatus.choices, default=LeaveStatus.PENDING)
    reason = models.TextField(blank=True, null=True)
    attachment = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'leave_application'

    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} - {self.leave_type.name}" 
 