from django.db import models
from ..core.base import TenantModel
from ..core.enums import CommonStatus

class AttendancePolicy(TenantModel):
    policy_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    late_arrival_grace_time = models.DurationField(null=True, blank=True)
    early_departure_grace_time = models.DurationField(null=True, blank=True)
    overtime_rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

    class Meta:
        db_table = 'attendance_policy'

    def __str__(self):
        return self.policy_name