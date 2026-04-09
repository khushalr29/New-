from rest_framework import serializers
from shared.models.meetings.meetings_attendee import MeetingAttendee

class MeetingAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAttendee
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            return attrs

        company = request.user.company
        meeting = attrs.get('meeting')
        employee = attrs.get('employee')

        if meeting and meeting.company != company:
            raise serializers.ValidationError({"meeting": "Unauthorized meeting selection."})
        
        if employee and employee.company != company:
            raise serializers.ValidationError({"employee": "Unauthorized employee selection."})

        return attrs