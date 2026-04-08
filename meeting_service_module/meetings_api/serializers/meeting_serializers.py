from rest_framework import serializers
from shared.models.meetings.meetings import Meeting
from shared.models.meetings.meetings_type import MeetingType
from shared.models.meetings.meeting_room import MeetingRoom
from shared.models.meetings.meetings_attendee import MeetingAttendee
from shared.models.meetings.meeting_minutes import MeetingMinutes
from shared.models.meetings.action_items import ActionItem

class MeetingTypeSerializer(serializers.ModelSerializer):
    """
    Serializes meeting categories (e.g., Internal, Client, Sprint).
    """
    class Meta:
        model = MeetingType
        fields = '__all__'

class MeetingRoomSerializer(serializers.ModelSerializer):
    """
    Serializes meeting room scheduling data.
    """
    class Meta:
        model = MeetingRoom
        fields = '__all__'

class MeetingAttendeeSerializer(serializers.ModelSerializer):
    """
    Handles mapping of employees/guests to specific meetings.
    """
    class Meta:
        model = MeetingAttendee
        fields = '__all__'

class MeetingMinutesSerializer(serializers.ModelSerializer):
    """
    Formats the textual outcome and recorded data from meetings.
    """
    class Meta:
        model = MeetingMinutes
        fields = '__all__'

class ActionItemSerializer(serializers.ModelSerializer):
    """
    Handles specific tasks/outcomes generated from meeting discussions.
    """
    class Meta:
        model = ActionItem
        fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
    """
    Main serializer for Meeting entity, handling relational lookups and multi-tenant logic.
    """
    attendee_count = serializers.IntegerField(source='attendees.count', read_only=True)
    
    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('company',)

    def create(self, validated_data):
        # We enforce tenant isolation by pinning the current user's company to the meeting record.
        user = self.context['request'].user
        if not user.company:
            raise serializers.ValidationError({"error": "Creating a meeting requires an active company association."})
            
        validated_data['company'] = user.company
        return super().create(validated_data)
