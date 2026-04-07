from django.db import models
from .contract_type import ContractType
from ..core.enums import CommonStatus
from ..core.base import TenantModel

class ContractTemplate(TenantModel):
    template_name = models.CharField(max_length=255)
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE, related_name='templates')
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    description = models.TextField(null=True, blank=True)
    is_set_default = models.BooleanField(default=False)
    contract = models.TextField()
    variables = models.CharField(max_length=255)

    class Meta:
        db_table = 'contract_template'

    def __str__(self):
        return self.template_name
