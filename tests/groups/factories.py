import factory
import factory.fuzzy
import factory.django
from core.models import Group


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText(length=50)

    class Meta:
        model = Group

    def __str__(self):
        return self.name
