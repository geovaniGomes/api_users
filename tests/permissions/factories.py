import factory.django
from permissions.models import CustomPermission

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomPermission

    name = "CRIAR USUARIO"
    code_name = "APIUSER::USSERS:WRITE"
