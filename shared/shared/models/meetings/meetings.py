from .meeting_room import MeetingRoom
from .meetings_type import MeetingType
from ..core.employee import Employee
from django.db import models
from ..core.enums import RecurrenceType

from ..core.base import TenantModel

class Meeting(TenantModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    meeting_type = models.ForeignKey(MeetingType, on_delete=models.SET_NULL, null=True, related_name='meetings')
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.SET_NULL, null=True, related_name='meetings')
    meeting_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    organizer = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='organized_meetings')
    recurrence = models.CharField(max_length=20, choices=RecurrenceType.choices)
    recurrence_end_date = models.DateField(null=True, blank=True)
    agenda = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'meeting'
        ordering = ['start_time']

    def __str__(self):
        return self.title