from django.utils import timezone
from rest_framework import viewsets
from .models import Product, Warehouse, Shelve, Inventory, InventoryMovement, WarehouseCreation, OrderCreation, AuditLog 
from .serializers import AuditLogSerializer
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response




class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all().order_by('-created_at')
    serializer_class = AuditLogSerializer
    
    @api_view(['POST'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def update_order(request, order_id):
        try:
            order = order_id.objects.get(id=order_id)
        except order_id.DoesNotExist:
            return Response({"error": "Pedido no encontrado"}, status=404)

        # guardar quién modifica
        order._modified_by = request.user

        # aplicar cambios
        status = request.data.get("status")
        quantity = request.data.get("quantity")

        if status:
            order.status = status
        if quantity:
            order.quantity = quantity

        order.save()
        return Response({"message": "Pedido actualizado correctamente"})


    @api_view(['GET'])
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def list_audit_logs(request):
        logs = AuditLog.objects.all().order_by("-created_at")
        data = [
            {
                "order": log.order_id,
                "user": log.user.username if log.user else "Desconocido",
                "action_type": log.action_type,
                "detail": log.detail,
                "created_at": log.created_at,
            }
            for log in logs
        ]
        return Response(data)
    
@require_http_methods(["GET", "HEAD"])
def health_check(request):

    res = JsonResponse({"status": "ok"})
    return _no_store(res)
