from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import AuditLog
from .serializers import AuditLogSerializer
from .filters import AuditLogFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.

class LogViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mencatat dan mengambil log aktivitas.
    
    create:
        Mencatat log aktivitas baru.
    
    list:
        Menampilkan daftar log dengan filter dan pagination.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AuditLogFilter
    ordering_fields = ['timestamp', 'user_id', 'entity', 'action']
    ordering = ['-timestamp']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        """
        Optionally restricts the returned logs by filtering
        based on query parameters.
        """
        queryset = AuditLog.objects.all()
        
        # Tambahan filter manual jika diperlukan
        user_id = self.request.query_params.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
            
        # Filter untuk range waktu
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date is not None and end_date is not None:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset
