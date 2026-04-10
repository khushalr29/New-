from rest_framework import serializers
from shared.models.time_tracking.time_entries import TimeEntries

class TimeEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntries
        fields = '__all__'

