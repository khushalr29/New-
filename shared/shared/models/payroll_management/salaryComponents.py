from django.db import models
from ..core.enums import CommonStatus, ComponentType, CalculationType
from ..core.base import TenantModel

class SalaryComponent(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    component_type = models.CharField(max_length=20, choices=ComponentType.choices)
    calculation_type = models.CharField(max_length=25, choices=CalculationType.choices)
    fixed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=15, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

    class Meta:
        db_table = 'salary_component'

    def __str__(self):
        return self.name
