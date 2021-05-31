from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

from ..models import User
from permissions.models import CustomPermission
from .serializers import MyTokenObtainPairSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):

        if request.data.get('permissions'):
            permissions = request.data['permissions']
            del request.data['permissions']
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer = associate_permissions(serializer.data['id'], permissions)

        elif request.data.get('permissions') == []:
            del request.data['permissions']
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data.get('permissions'):
            permissions = request.data['permissions']

            permission_valid(permissions)

            del request.data['permissions']
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            serializer = associate_permissions(serializer.data['id'], permissions)
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(serializer.data)


def permission_valid(permissions):
    for new_permission in permissions:
        get_object_or_404(CustomPermission, code_name=new_permission['code_name'])


def associate_permissions(pk, permissions):
    list_permissions = []

    for new_permission in permissions:
        permission = CustomPermission.objects.get(code_name=new_permission['code_name'])
        list_permissions.append(permission)

    user = User.objects.get(id=pk)
    user.permissions.set(permissions)
    user.save()
    serializer = UserSerializer(user)
    return serializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
