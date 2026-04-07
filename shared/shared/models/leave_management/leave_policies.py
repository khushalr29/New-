from django.db import models
from .leave_type import LeaveType
from ..core.enums import CommonStatus , AccrualType

from ..core.base import TenantModel

class LeavePolicy(TenantModel):
    policy_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave_policies')
    accrual_type = models.CharField(max_length=20, choices=AccrualType.choices)
    accrual_rate = models.PositiveIntegerField()
    carry_forward_limit  = models.PositiveIntegerField()
    min_days_per_application = models.PositiveIntegerField()
    max_days_per_application = models.PositiveIntegerField()
    is_required_approval = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices= CommonStatus.choices)

    class Meta:
        db_table = 'leave_policy'
        ordering = ['policy_name']
        unique_together = ('policy_name', 'company')

    def __str__(self):
        return self.policy_name