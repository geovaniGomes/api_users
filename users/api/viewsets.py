from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


from ..models import User
from permissions.models import CustomPermission
from .serializers import MyTokenObtainPairSerializer, UserSerializer


class UserVieweSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = None
        if request.data.get('permissions'):
            permissions = request.data['permissions']
            del request.data['permissions']
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializer = associate_permissions(serializer.data['id'], permissions)
        else:
            request.data['permissions'] = []
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print(request.data['id'])

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = None
        if request.data.get('permissions'):
            permissions = request.data['permissions']
            del request.data['permissions']
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            serializer = associate_permissions(serializer.data['id'], permissions)
        else:
            request['permissions'] = []
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(serializer.data)

def associate_permissions(pk, permissions):
    list_permissions = []

    for new_permission in permissions:
        permission = get_object_or_404(CustomPermission, code_name=new_permission['code_name'])
        list_permissions.append(permission)

    user = User.objects.get(id=pk)
    user.permissions.set(list_permissions)
    user.save()
    serializer = UserSerializer(user)
    return serializer




class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

