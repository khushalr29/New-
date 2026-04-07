from django.db import models
from .meetings import Meeting
from ..core.employee import Employee
from ..core.enums import AttendanceStatus, AttendenceType, RSVPStatus

class MeetingAttendee(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendees')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='meeting_attendances')
    attendance_type = models.CharField(max_length=20, choices=AttendenceType.choices)
    rsvp_status = models.CharField(max_length=20, choices=RSVPStatus.choices)
    attendance_status = models.CharField(max_length=20, choices=AttendanceStatus.choices)
    decline_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'meeting_attendee'
        unique_together = ('meeting', 'employee')