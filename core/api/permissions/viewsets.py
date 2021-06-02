from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from core.models import Permission, Group
from .serializers import PermissionSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


def is_permission(permission, pk=None):
    data = {}
    if pk:
        exist = Permission.objects.filter(code_name=permission['code_name']).exclude(id__in=[pk]).exists()
    else:
        exist = Permission.objects.filter(code_name=permission['code_name']).exists()

    if exist:
        data = {"detail": "permission already registered."}
        return data
    return data


def is_group(groups):
    for group in groups:
        get_object_or_404(Group, name=group['name'], is_deleted=False)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def create(self, request, *args, **kwargs):
        if len(request.data) == 0:
            response = {
                "name": "This field may not be blank.",
                "code_name": "This field may not be blank."
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        permission = request.data
        data = is_permission(permission)
        if not data:
            groups = request.data.get('groups')

            if groups is not None and groups != []:
                is_group(groups)

            serializer = self.serializer_class(data=permission)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if len(request.data) == 0:
            response = {
                "name": "This field may not be blank.",
                "code_name": "This field may not be blank."
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        permission = request.data
        data = is_permission(permission, kwargs.get('pk'))

        if not data:

            partial = kwargs.pop('partial', False)
            instance = self.get_object()

            groups = request.data.get('groups')

            if groups is not None and groups != []:
                is_group(groups)

            serializer = self.serializer_class(instance, data=permission, partial=partial)
            serializer.is_valid(raise_exception=True)

            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        permission = get_object_or_404(Permission, id=pk)
        permission.inactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)
