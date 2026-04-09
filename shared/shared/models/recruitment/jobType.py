from django.db import models
from ..core.enums import CommonStatus
from ..core.base import TenantModel

class JobType(TenantModel):
    job_type_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=CommonStatus.choices)

    class Meta:
        db_table = 'job_type'
        unique_together = ('job_type_name', 'company')

    def __str__(self):
        return self.job_type_name


                                     