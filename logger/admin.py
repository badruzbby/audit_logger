from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'action', 'entity', 'entity_id', 'log_level', 'timestamp')
    list_filter = ('action', 'entity', 'log_level', 'timestamp')
    search_fields = ('user_id', 'entity', 'entity_id')
    readonly_fields = ('id', 'timestamp')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    
    def has_change_permission(self, request, obj=None):
        # Audit logs should not be modified
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete audit logs
        return request.user.is_superuser
