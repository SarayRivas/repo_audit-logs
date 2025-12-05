from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    ACTION_TYPES = [
        ('cambio_estado', 'Cambio de Estado'),
        ('cambio_inventario', 'Cambio de Inventario'),
        ('despacho', 'Despacho'),
    ]

    order_number = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    detail = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.user} - {self.action_type} - {self.order_number}"