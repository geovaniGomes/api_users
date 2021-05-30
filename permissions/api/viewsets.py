from rest_framework.viewsets import ModelViewSet

from ..models import CustomPermission
from .serializers import PermissionSerializer


class PermissionVieweSet(ModelViewSet):
    queryset = CustomPermission.objects.all()
    serializer_class = PermissionSerializer
