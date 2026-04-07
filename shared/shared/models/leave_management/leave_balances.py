from django.db import models
from .leave_type import LeaveType
from ..core.base import TenantModel

class LeaveBalance(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_balances')
    year = models.PositiveIntegerField()
    allocated_days = models.PositiveIntegerField()
    carry_forwarded_days = models.PositiveIntegerField(default=0)
    manual_adjustment = models.PositiveIntegerField(default=0)
    adjustment_reason = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'leave_balance'
        unique_together = ('employee', 'leave_type', 'company')

    def __str__(self):
        return f"{self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'} - {self.leave_type.name if hasattr(self.leave_type, 'name') else 'Leave'}"