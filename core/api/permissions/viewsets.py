from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from core.models import Permission, Group
from .serializers import PermissionSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


def is_group(groups):
    for group in groups:
        get_object_or_404(Group, name=group['name'], is_deleted=False)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        permission = request.data
        groups = request.data.get('groups')

        if groups is not None and groups != []:
            is_group(groups)

        serializer = self.serializer_class(data=permission)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        permission = request.data
        groups = request.data.get('groups')

        if groups is not None and groups != []:
            is_group(groups)

        serializer = self.serializer_class(instance, data=permission, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        permission = get_object_or_404(Permission, id=pk)
        permission.inactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)
