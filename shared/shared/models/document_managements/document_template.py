from django.db import models
from .document_categories import DocumentCategories
from ..core.enums import CommonStatus, DocumentExtensions
from ..core.base import TenantModel

class DocumentTemplate(TenantModel):
    template_name = models.CharField(max_length=255)
    category = models.ForeignKey(DocumentCategories, on_delete=models.CASCADE, related_name='document_templates')
    file_format = models.CharField(max_length=5, choices=DocumentExtensions.choices, default=DocumentExtensions.PDF)
    status = models.CharField(max_length=15, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    description = models.TextField(null=True, blank=True)
    is_set_default_category = models.BooleanField(default=False)
    content = models.TextField()
    placeholder = models.TextField()
    default_values = models.TextField()

    class Meta:
        db_table = 'document_template'

    def __str__(self):
        return self.template_name