from rest_framework import serializers
from shared.models.meetings.action_items import ActionItem

class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or not request.user:
            return attrs

        company = request.user.company
        meeting = attrs.get('meeting')
        assigned_to = attrs.get('assigned_to')

        if meeting and meeting.company != company:
            raise serializers.ValidationError({"meeting": "Unauthorized meeting selection."})
        
        if assigned_to and assigned_to.company != company:
            raise serializers.ValidationError({"assigned_to": "Unauthorized employee assignment."})

        return attrs