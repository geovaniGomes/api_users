from core.api.permissions.serializers import PermissionSerializer
from core.api.groups.serializers import GroupSerializer
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from core.models import User, Permission, Group


class UserSerializer(serializers.ModelSerializer):

    permissions = PermissionSerializer(many=True, required=False)
    groups = GroupSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'password',
                  'permissions',
                  'groups']
        extra_kwargs = {'password': {'write_only': True}}

    def associate_permissions(self, pk, new_permissions):
        list_permissions = []
        for new_permission in new_permissions:
            permission = Permission.objects.get(code_name=new_permission['code_name'],
                                                is_deleted=False)
            list_permissions.append(permission)

        user = User.objects.get(id=pk)
        user.permissions.set(list_permissions)
        user.save()
        return user

    def associate_groups(self, pk, new_groups):
        list_groups = []
        for new_group in new_groups:
            group = Group.objects.get(name=new_group['name'], is_deleted=False)
            list_groups.append(group)

        user = User.objects.get(id=pk)
        user.groups.set(list_groups)
        user.save()

    def create(self, validated_data):
        permissions = validated_data.get('permissions')
        groups = validated_data.get('groups')
        password = validated_data['password']
        del validated_data['password']

        if groups is not None and groups != []:
            del validated_data['groups']
        
        if permissions is not None and permissions != []:
            del validated_data['permissions']

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        if groups is not None:
            self.associate_groups(user.id, groups)

        if permissions is not None:
            self.associate_permissions(user.id, permissions)

        return user

    def update(self, instance, validated_data):

        permissions = validated_data.get('permissions')
        groups = validated_data.get('groups')

        if groups is not None and groups != []:
            del validated_data['groups']

        if permissions is not None and permissions != []:
            del validated_data['permissions']

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()

        if groups is not None:
            self.associate_groups(instance.id, groups)

        if permissions is not None:
            self.associate_permissions(instance.id, permissions)

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        user_id = JWTTokenUserAuthentication.get_user(cls, token)
        usuario_logado = User.objects.get(username=user)

        # Add custom claims
        token['username'] = usuario_logado.username
        token['first_name'] = usuario_logado.first_name
        token['last_name'] = usuario_logado.last_name
        token['email'] = usuario_logado.email
        return token


