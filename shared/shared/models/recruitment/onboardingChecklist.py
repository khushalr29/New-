from django.db import models
from ..core.enums import CommonStatus
from ..core.base import TenantModel

class OnboardingChecklist(TenantModel):
    checklist_name = models.CharField(max_length=255)
    description = models.TextField(null= True, blank= True)
    is_set_default = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

    class Meta:
        db_table = 'onboarding_checklist'
        unique_together = ('checklist_name', 'company')

    def __str__(self):
        return self.checklist_name