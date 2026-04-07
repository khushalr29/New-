from django.db import models
from ..core.enums import PayrollFrequencyEnum
from ..core.base import TenantModel

class PayrollRun(TenantModel):
    title = models.CharField(max_length=255)
    payroll_frequency = models.CharField(max_length=20, choices=PayrollFrequencyEnum.choices, default=PayrollFrequencyEnum.MONTHLY)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    pay_date = models.DateField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'payroll_run'

    def __str__(self):
        return f"{self.title} ({self.pay_period_start} - {self.pay_period_end})"
