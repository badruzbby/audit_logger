import django_filters
from .models import AuditLog

class AuditLogFilter(django_filters.FilterSet):
    user_id = django_filters.NumberFilter(lookup_expr='exact')
    entity = django_filters.CharFilter(lookup_expr='icontains')
    entity_id = django_filters.CharFilter(lookup_expr='exact')
    action = django_filters.CharFilter(lookup_expr='exact')
    log_level = django_filters.CharFilter(lookup_expr='exact')
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = AuditLog
        fields = ['user_id', 'entity', 'entity_id', 'action', 'log_level', 'timestamp_after', 'timestamp_before'] 