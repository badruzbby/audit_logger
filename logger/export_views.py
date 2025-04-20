import csv
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog
from .filters import AuditLogFilter

class ExportLogsCSVView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Apply filters
        filterset = AuditLogFilter(request.GET, queryset=AuditLog.objects.all())
        queryset = filterset.qs
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'User ID', 'Action', 'Entity', 'Entity ID', 
                         'Changes', 'Timestamp', 'Log Level'])
        
        for log in queryset:
            writer.writerow([
                log.id,
                log.user_id,
                log.action,
                log.entity,
                log.entity_id,
                json.dumps(log.changes),
                log.timestamp.isoformat(),
                log.log_level
            ])
        
        return response

class ExportLogsJSONView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Apply filters
        filterset = AuditLogFilter(request.GET, queryset=AuditLog.objects.all())
        queryset = filterset.qs
        
        logs = []
        for log in queryset:
            logs.append({
                'id': log.id,
                'user_id': log.user_id,
                'action': log.action,
                'entity': log.entity,
                'entity_id': log.entity_id,
                'changes': log.changes,
                'timestamp': log.timestamp.isoformat(),
                'log_level': log.log_level
            })
        
        response = JsonResponse(logs, safe=False)
        response['Content-Disposition'] = 'attachment; filename="audit_logs.json"'
        return response 