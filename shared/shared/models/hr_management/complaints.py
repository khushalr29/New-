from django.db import models
from ..core.employee import Employee
from ..core.enums import ComplaintStatus, ComplaintType

from ..core.base import TenantModel

class Complaint(TenantModel):
    complainant = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='complaints')
    against_employee = models.ForeignKey('shared.Employee', on_delete=models.CASCADE, related_name='complaints_against')
    complaint_type = models.CharField(max_length=255, choices=ComplaintType.choices)
    subject = models.CharField(max_length=255)
    complaint_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=ComplaintStatus.choices, default=ComplaintStatus.OPEN)
    resolution_details = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey('shared.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_resolved')
    is_submit_anonymously = models.BooleanField(default=False)

    class Meta:
        db_table = 'complaint'
        ordering = ['-created_at']

    def __str__(self):
        return f"Complaint by {self.complainant.full_name} - {self.subject} ({self.status})"