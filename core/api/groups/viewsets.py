from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from core.api.groups.serializers import GroupSerializer
from core.models import Group


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        group = get_object_or_404(Group, id=pk)
        group.inactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)
