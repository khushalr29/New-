from django.db import models
from ..core.enums import CommonStatus

from ..core.base import TenantModel

class LeaveType(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    max_days_per_year = models.PositiveIntegerField()
    color = models.CharField(max_length=7, default="#4A42F0")
    paid_leave = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices= CommonStatus.choices)
