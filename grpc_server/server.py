import os
import sys
import json
import time
import grpc
import django
from concurrent import futures

# Tambahkan path project untuk import Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audit_logger_project.settings")
django.setup()

# Import generated protobuf code
from grpc_server.generated import logger_pb2, logger_pb2_grpc

# Import Django models
from logger.models import AuditLog, ActionChoices, LogLevel

class LogServiceServicer(logger_pb2_grpc.LogServiceServicer):
    def LogAction(self, request, context):
        try:
            # Konversi action dari enum protobuf ke string Django
            action_map = {
                logger_pb2.Action.CREATE: ActionChoices.CREATE,
                logger_pb2.Action.UPDATE: ActionChoices.UPDATE,
                logger_pb2.Action.DELETE: ActionChoices.DELETE,
            }
            
            action = action_map.get(request.action, ActionChoices.CREATE)
            
            # Parse changes dari JSON string
            try:
                changes = json.loads(request.changes)
            except json.JSONDecodeError:
                changes = {"error": "Invalid JSON format", "raw": request.changes}
            
            # Set default log level ke INFO jika tidak ada
            log_level = request.log_level if request.log_level else LogLevel.INFO
            
            # Buat log entry
            log_entry = AuditLog.objects.create(
                user_id=request.user_id,
                action=action,
                entity=request.entity,
                entity_id=request.entity_id,
                changes=changes,
                log_level=log_level
            )
            
            # Return response
            return logger_pb2.LogResponse(
                success=True,
                log_id=str(log_entry.id),
                message="Log entry successfully created"
            )
        except Exception as e:
            return logger_pb2.LogResponse(
                success=False,
                log_id="",
                message=f"Error: {str(e)}"
            )

def serve():
    # Buat server gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger_pb2_grpc.add_LogServiceServicer_to_server(LogServiceServicer(), server)
    
    # Ambil port dari environment variable atau default ke 50051
    port = os.environ.get("GRPC_PORT", "50051")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    
    print(f"gRPC server started on port {port}")
    
    try:
        while True:
            time.sleep(86400)  # 1 day in seconds
    except KeyboardInterrupt:
        server.stop(0)
        print("gRPC server stopped")

if __name__ == "__main__":
    serve() 