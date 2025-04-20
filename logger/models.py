from django.db import models

class ActionChoices(models.TextChoices):
    CREATE = 'CREATE', 'Create'
    UPDATE = 'UPDATE', 'Update'
    DELETE = 'DELETE', 'Delete'

class LogLevel(models.TextChoices):
    INFO = 'INFO', 'Info'
    WARNING = 'WARNING', 'Warning'
    ERROR = 'ERROR', 'Error'
    CRITICAL = 'CRITICAL', 'Critical'

class AuditLog(models.Model):
    user_id = models.IntegerField(db_index=True)
    action = models.CharField(max_length=20, choices=ActionChoices.choices, db_index=True)
    entity = models.CharField(max_length=100, db_index=True)
    entity_id = models.CharField(max_length=100, db_index=True)
    changes = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    log_level = models.CharField(max_length=20, choices=LogLevel.choices, 
                                 default=LogLevel.INFO)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user_id', 'action']),
            models.Index(fields=['entity', 'entity_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.action} on {self.entity}:{self.entity_id} by user:{self.user_id}"
