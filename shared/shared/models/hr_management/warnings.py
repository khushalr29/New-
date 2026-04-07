from django.db import models
from ..core.base import TenantModel
from ..core.enums import WarningType, WarningSeverity

class Warning(TenantModel):
    warning_by = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='warnings_given')
    warning_to = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='warnings_received')
    warning_type = models.CharField(max_length=50, choices=WarningType.choices)
    subject = models.CharField(max_length=255)
    severity = models.CharField(max_length=50, choices=WarningSeverity.choices)
    warning_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    has_improvement_plan = models.BooleanField(default=False)
    improvement_plan_goal = models.TextField(blank=True, null=True)
    improvement_plan_start_date = models.DateField(null=True, blank=True)
    improvement_plan_end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'warning'
        ordering = ['-warning_date']

    def __str__(self):
        return f"{self.subject} - {self.warning_to.full_name if hasattr(self.warning_to, 'full_name') else 'Employee'}"