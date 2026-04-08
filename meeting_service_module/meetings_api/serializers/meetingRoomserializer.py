from rest_framework import serializers
from shared.models.meetings.meeting_room import MeetingRoom

class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'
        read_only_fields = ['company']