import factory.django
from core.models import Permission


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission



