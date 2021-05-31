from permissions.api.serializers import PermissionSerializer
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from ..models import User


class UserSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'is_active',
                  'is_staff',
                  'password',
                  'permissions']

    def create(self, validated_data):

        password = validated_data['password']
        del validated_data['password']

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()

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
    

