import factory.django
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "leticia_calderaro"
    first_name = "leticia"
    last_name = "brandao"
    email = "let@gmail.com"
    password = "52002600NN"
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
