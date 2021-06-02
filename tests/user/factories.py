import factory.django
from core.models import User
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "leticia_calderaro"
    first_name = "leticia"
    last_name = "brandao"
    email = "let@gmail.com"
    password = "52002600NN"
    is_staff = False


class UserSecondaryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.fuzzy.FuzzyText(length=50)
    first_name = factory.fuzzy.FuzzyText(length=100)
    last_name = factory.fuzzy.FuzzyText(length=100)
    email = factory.LazyAttribute(lambda obj: "%s@example.com" % obj.name)
    password = factory.fuzzy.FuzzyText(length=50)
    is_staff = False


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "admin"
    first_name = "admin_user"
    last_name = "user"
    email = "admion@gmail.com"
    password = "52002600NN"
    is_staff = True
