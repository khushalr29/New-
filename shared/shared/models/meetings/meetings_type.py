from django.db import models
from ..core.enums import CommonStatus

from ..core.base import TenantModel

class MeetingType(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7)
    default_duration= models.PositiveIntegerField(help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)

    class Meta:
        db_table = 'meeting_type'
        ordering = ['name']

    def __str__(self):
        return self.name