from rest_framework import serializers
from shared.models.meetings.meetings_type import MeetingType
from shared.utils.common.validation import validate_name

class MeetingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingType
        fields = '__all__'
        read_only_fields = ['company']

    def validate_name(self, value):
        return validate_name(value, field_name="Meeting Type Name")