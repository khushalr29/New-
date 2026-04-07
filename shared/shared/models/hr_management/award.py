from django.db import models
from .hr_masters import AwardType
from ..core.base import TenantModel

class Award(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='awards')
    award_type = models.ForeignKey(AwardType, on_delete=models.SET_NULL, null=True, related_name='awards')
    date_awarded = models.DateField()
    gift = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    photo = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'award'
        ordering = ['-date_awarded']

    def __str__(self):
        return f"{self.employee.full_name} - {self.award_type.award_type if self.award_type else 'Award'}"