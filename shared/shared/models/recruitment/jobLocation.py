from django.db import models
from ..core.enums import CommonStatus
from ..core.base import TenantModel

class JobLocation(TenantModel):
    job_location = models.CharField(max_length=255, null=True, blank=True)
    is_remote_work = models.BooleanField(default=False)
    address = models.TextField()
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=10, choices=CommonStatus.choices)

    class Meta:
        db_table = 'job_location'
        unique_together = ('job_location', 'company')

    def __str__(self):
        return self.job_location
