from django.db import models
from ..core.enums import CommonStatus
from .onboardingChecklist import OnboardingChecklist
from .jobCategories import JobCategory

class ChecklistItem(models.Model):
    checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE, related_name='checklist')
    task_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='category')
    is_required_task = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
