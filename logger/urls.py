from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogViewSet
from .export_views import ExportLogsCSVView, ExportLogsJSONView

router = DefaultRouter()
router.register(r'', LogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('export/csv/', ExportLogsCSVView.as_view(), name='export-logs-csv'),
    path('export/json/', ExportLogsJSONView.as_view(), name='export-logs-json'),
] 