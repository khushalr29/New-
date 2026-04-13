from django.db import models
from .document_categories import DocumentCategories
from ..core.base import TenantModel

class HRDocument(TenantModel):
    document_title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(DocumentCategories, on_delete=models.CASCADE, related_name='hr_documents')
    file = models.TextField()
    effective_date = models.DateField()
    expiry_date = models.DateField()
    is_requires_acknowledgement = models.BooleanField(default=False)

    class Meta:
        db_table = 'hr_document'
        unique_together = ('document_title', 'company')

    def __str__(self):
        return self.document_title