from django.db import models
from ..core.enums import MeetingType, CommonStatus

from ..core.base import TenantModel

class MeetingRoom(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=MeetingType.choices)
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField()
    equipment = models.TextField(blank=True, null=True)
    booking_url = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=CommonStatus.choices, default=CommonStatus.ACTIVE)
