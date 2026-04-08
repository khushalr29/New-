from django.db import models
from .onboardingChecklist import OnboardingChecklist
from ..core.employee import Employee
from ..core.base import TenantModel

class Onboarding(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='onboarding_employee')
    onboarding_checklist = models.ForeignKey(OnboardingChecklist, on_delete=models.CASCADE , related_name='onboarding_checklist')
    start_date = models.DateField()
    buddy_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='buddy_employee')

    class Meta:
        db_table = 'onboarding'
        unique_together = ('employee', 'company')

    def __str__(self):
        return f"Onboarding - {self.employee}"