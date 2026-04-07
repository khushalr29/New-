from django.db import models
from .document_categories import DocumentCategories

class HRDocument(models.Model):
    document_title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(DocumentCategories, on_delete=models.CASCADE, related_name='hr_document')
    file = models.TextField()
    effective_date = models.DateField()
    expiry_date = models.DateField()
    is_requires_acknowledgement = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
