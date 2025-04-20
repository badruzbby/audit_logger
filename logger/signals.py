import json
import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AuditLog

@receiver(post_save, sender=AuditLog)
def trigger_webhook(sender, instance, created, **kwargs):
    """
    Trigger webhook for specified actions
    """
    # Check if webhook is enabled
    if not settings.WEBHOOK_ENABLED or not settings.WEBHOOK_URL:
        return
    
    # Check if action should trigger webhook
    if instance.action not in settings.WEBHOOK_ACTIONS:
        return
    
    # Prepare webhook data
    webhook_data = {
        'id': instance.id,
        'user_id': instance.user_id,
        'action': instance.action,
        'entity': instance.entity,
        'entity_id': instance.entity_id,
        'changes': instance.changes,
        'timestamp': instance.timestamp.isoformat(),
        'log_level': instance.log_level
    }
    
    # Send webhook
    try:
        response = requests.post(
            settings.WEBHOOK_URL,
            json=webhook_data,
            headers={'Content-Type': 'application/json'},
            timeout=5.0  # 5 second timeout
        )
        response.raise_for_status()
    except Exception as e:
        # Log error but don't halt execution
        print(f"Webhook error: {str(e)}") 