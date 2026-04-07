from django.db import models
from ..core.enums import CommonStatus

class JobLocation(models.Model):
    job_location = models.CharField(max_length=255,null=True, blank=True)
    is_remote_work = models.BooleanField(default=False)
    address = models.TextField()
    city = models.CharField(max_length=255,null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    country = models.CharField(max_length=255,null=True, blank=True)
    postal_code = models.CharField(max_length=255,null=True, blank=True)
    status = models.CharField(max_length=10, choices=CommonStatus.choices)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
