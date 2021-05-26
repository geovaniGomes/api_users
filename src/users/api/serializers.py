from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        user_id =JWTTokenUserAuthentication.get_user(cls,token)
        usuario_logado = User.objects.get(username=user)

        # Add custom claims
        token['username'] = usuario_logado.username
        token['first_name'] = usuario_logado.first_name
        token['last_name'] = usuario_logado.last_name
        token['email'] = usuario_logado.email
        return token
    

