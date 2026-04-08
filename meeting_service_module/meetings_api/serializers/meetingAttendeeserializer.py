from rest_framework import serializers
from shared.models.meetings.meetings_attendee import MeetingAttendee

class MeetingAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAttendee
        fields = '__all__'