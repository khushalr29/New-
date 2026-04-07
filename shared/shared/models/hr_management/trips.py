from django.db import models
from ..core.base import TenantModel

class Trip(TenantModel):
    employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    purpose_of_trip = models.CharField(max_length=255)
    place_of_visit = models.CharField(max_length=255)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    advance_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    expected_outcomes = models.TextField(blank=True, null=True)
    documents = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Planned')

    class Meta:
        db_table = 'trip'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} to {self.place_of_visit}"