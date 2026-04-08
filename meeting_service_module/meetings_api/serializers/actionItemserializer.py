from rest_framework import serializers
from shared.models.meetings.action_items import ActionItem

class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = '__all__'