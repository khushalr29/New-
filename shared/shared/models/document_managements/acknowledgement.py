from django.db import models
from .hr_document import HRDocument
from ..core.employee import Employee

class Acknowledgement(models.Model):
    document = models.ForeignKey(HRDocument, on_delete=models.CASCADE, related_name='acknowledgement')
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='user_acknowledgement')
    due_date = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

