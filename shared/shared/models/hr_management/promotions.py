from django.db import models
from ..core.enums import PromotionStatus
from ..core.base import TenantModel

class Promotion(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='promotions')
    promotion_title = models.CharField(max_length=255)
    description = models.TextField()
    promotion_date = models.DateField()
    old_designation = models.ForeignKey('shared.Designation', on_delete=models.CASCADE, related_name='promotions_old')
    new_designation = models.ForeignKey('shared.Designation', on_delete=models.CASCADE, related_name='promotions_new')
    salary_adjustment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    reason_for_promotion = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PromotionStatus.choices, default=PromotionStatus.PENDING)

    class Meta:
        db_table = 'promotion'
        ordering = ['-promotion_date']

    def __str__(self):
        return f"{self.promotion_title} - {self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'}"
