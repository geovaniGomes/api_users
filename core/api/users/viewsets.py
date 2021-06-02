from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import action
from django.db.models import Q

from core.models import User, Permission, Group

from .serializers import MyTokenObtainPairSerializer, UserSerializer


def is_group(groups):
    for group in groups:
        get_object_or_404(Group, name=group['name'], is_deleted=False)


def is_permission(permissions):
    for permission in permissions:
        get_object_or_404(Permission, code_name=permission['code_name'], is_deleted=False)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        groups = request.data.get('groups')
        permissions = request.data.get('permissions')

        if groups and len(groups) > 0:
            is_group(groups)

        if permissions and len(permissions) > 0:
            is_permission(permissions)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.initial_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        groups = request.data.get('groups')
        permissions = request.data.get('permissions')

        if groups is not None and groups != []:
            is_group(groups)

        if permissions is not None and permissions != []:
            is_permission(permissions)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(User, id=pk)
        user.inactivate()
        return Response(status=status.HTTP_204_NO_CONTENT)











class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
