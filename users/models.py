from django.contrib.auth.models import AbstractUser
from django.db import models
from permissions.models import CustomPermission


class User(AbstractUser):
    permissions = models.ManyToManyField(CustomPermission, null=True, blank=True)
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    email = models.EmailField('email address', blank=False, unique=True)
    password = models.CharField('password', max_length=128, null=False)
