from rest_framework import serializers
from shared.models.meetings.meetings_type import MeetingType

class MeetingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingType
        fields = '__all__'
        read_only_fields = ['company']