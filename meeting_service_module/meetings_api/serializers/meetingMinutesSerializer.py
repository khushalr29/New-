from rest_framework import serializers
from shared.models.meetings.meeting_minutes import MeetingMinutes

class MeetingMinutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMinutes
        fields = '__all__'
        read_only_fields = ['company']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            return attrs

        company = request.user.company
        meeting = attrs.get('meeting')

        if meeting and meeting.company != company:
            raise serializers.ValidationError({"meeting": "Unauthorized meeting selection."})

        return attrs