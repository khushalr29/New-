from django.db import models
from ..core.base import TenantModel

class Transfer(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='transfers')
    transfer_title = models.CharField(max_length=255)
    description = models.TextField()
    transfer_date = models.DateField()
    old_department = models.ForeignKey('shared.Department', on_delete=models.CASCADE, related_name='transfers_old')
    new_department = models.ForeignKey('shared.Department', on_delete=models.CASCADE, related_name='transfers_new')
    old_branch = models.ForeignKey('shared.Branch', on_delete=models.CASCADE, related_name='transfers_old')
    new_branch = models.ForeignKey('shared.Branch', on_delete=models.CASCADE, related_name='transfers_new')

    class Meta:
        db_table = 'transfer'
        ordering = ['-transfer_date']

    def __str__(self):
        return f"{self.transfer_title} - {self.employee.full_name if hasattr(self.employee, 'full_name') else 'Employee'}"