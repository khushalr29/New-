from django.db import models
from ..core.enums import CommonStatus

from ..core.base import TenantModel

class ContractType(TenantModel):
    contract_type_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    default_duration_months = models.PositiveIntegerField(default=0)
    probation_period = models.PositiveIntegerField(default=0)
    notice_period = models.PositiveIntegerField(default=1)
    is_renewable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

    def __str__(self):
        return self.contract_type_name

    