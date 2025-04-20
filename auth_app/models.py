from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class UserAPIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def has_expired(self):
        if not self.expires:
            return False
        return timezone.now() > self.expires
    
    def is_valid(self):
        return self.is_active and not self.has_expired()
    
    class Meta:
        ordering = ['-created']
