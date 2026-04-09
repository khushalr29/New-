from rest_framework import serializers
from shared.models.meetings.meetings import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ['company']

    def validate(self, data):
        """
        Check that start_time is before end_time.
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError({
                    "end_time": "End time must be after start time."
                })
        
        return data
       
