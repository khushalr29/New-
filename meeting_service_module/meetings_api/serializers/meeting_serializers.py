from rest_framework import serializers
from shared.models.meetings.meetings import Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ['company']
       
