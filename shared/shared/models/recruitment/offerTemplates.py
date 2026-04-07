from django.db import models
from ..core.enums  import CommonStatus

class OfferTemplates(models.Model):
    template_name =models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
    template_content = models.TextField()
    variables = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)