from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from core.api.groups.serializers import GroupSerializer
from core.models import Group


def is_group(group, pk=None):
    data = {}
    if pk:
        exist = Group.objects.filter(name=group).exclude(id__in=[pk]).exists()
    else:
        exist = Group.objects.filter(name=group).exists()

    if exist:
        data = {"detail": "group already registered."}
        return data
    return data


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        group = request.data.get('name')
        data = {"name": "name field is required."}

        if group is None:
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
        elif group.isspace():
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            data = is_group(group)

            if not data:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        group = request.data.get('name')
        data = {"name": "name field is required."}

        if group is None:
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
        elif group.isspace():
            return Response(data=data,
                            status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)
        else:
            data = is_group(group, kwargs['pk'])

            if not data:
                partial = kwargs.pop('partial', False)
                instance = self.get_object()

                serializer = self.serializer_class(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)

                self.perform_update(serializer)
                return Response(serializer.data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        group = get_object_or_404(Group, id=pk)
        group.inactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)
