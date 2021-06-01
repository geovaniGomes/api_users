import factory.django
from core.models import Permission


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    name = "CRIAR USUARIO"
    code_name = "APIUSER::USSERS:WRITE"
