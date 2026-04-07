from django.db import models
from ..core.enums import MeetingMinutesType
from ..core.base import TenantModel

class MeetingMinutes(TenantModel):
    meeting = models.ForeignKey('shared.Meeting', on_delete=models.CASCADE, related_name='minutes')
    topic = models.CharField(max_length=255)
    minutes_type = models.CharField(max_length=20, choices=MeetingMinutesType.choices)
    content = models.TextField()
    recorded_by = models.ForeignKey('shared.Employee', on_delete=models.SET_NULL, null=True, related_name='recorded_minutes')
    recorded_date = models.DateField()
    recorded_time = models.TimeField()

    class Meta:
        db_table = 'meeting_minutes'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.topic} ({self.minutes_type})"