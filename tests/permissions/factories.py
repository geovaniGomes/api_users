import string
import factory
import factory.fuzzy
from core.models import Permission


class PermissionFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=50)
    code_name = factory.fuzzy.FuzzyText(length=100)

    class Meta:
        model = Permission


class PermissionWithGroup(factory.django.DjangoModelFactory):

    class Meta:
        model = Permission

    name = "screen users"
    code_name = "SCREEN::USERS:WRITE"