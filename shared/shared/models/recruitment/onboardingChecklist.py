from django.db import models
from ..core.enums import CommonStatus

class OnboardingChecklist(models.Model):
    checklist_name = models.CharField(max_length=255)
    description = models.TextField(null= True, blank= True)
    is_set_default = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)