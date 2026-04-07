from ..core.employee import Employee
from django.db import models

from ..core.base import TenantModel

class TimeEntries(TenantModel):
    employee= models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='time_entries')
    date = models.DateField()
    hours = models.PositiveIntegerField()
    project = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
