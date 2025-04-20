from rest_framework import serializers
from .models import AuditLog, ActionChoices, LogLevel

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user_id', 'action', 'entity', 'entity_id', 'changes', 'timestamp', 'log_level']
        read_only_fields = ['id', 'timestamp']

    def validate_action(self, value):
        if value not in ActionChoices:
            raise serializers.ValidationError(f"Action must be one of {ActionChoices.names}")
        return value

    def validate_log_level(self, value):
        if value not in LogLevel:
            raise serializers.ValidationError(f"Log level must be one of {LogLevel.names}")
        return value

    def validate_changes(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Changes must be a valid JSON object")
        return value 