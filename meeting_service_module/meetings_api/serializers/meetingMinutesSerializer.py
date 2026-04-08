from rest_framework import serializers
from shared.models.meetings.meeting_minutes import MeetingMinutes

class MeetingMinutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinutes
        fields = '__all__'
        read_only_fields = ['company']