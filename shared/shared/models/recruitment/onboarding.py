from django.db import models
from .onboardingChecklist import OnboardingChecklist
from ..core.employee import Employee

class Onboarding(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='onboarding_employee')
    onboarding_checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE , related_name='onboarding_checklist')
    start_date = models.DateField()
    buddy_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='buddy_employee')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)