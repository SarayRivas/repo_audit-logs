from rest_framework import serializers
from . import models

class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('order_number', 'user', 'action_type', 'detail', 'created_at',)
        model = models.AuditLog
    