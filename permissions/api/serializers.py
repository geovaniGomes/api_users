from rest_framework import serializers

from ..models import CustomPermission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ['id', 'code_name']
