import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class ClassBaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class ClassBase(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    objects = ClassBaseManager()

    class Meta:
        abstract = True

    def inactivate(self):
        self.is_deleted = True
        self.save()


class Group(ClassBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "group"
        verbose_name_plural = "groups"
        db_table = 'groups'

    name = models.CharField(max_length=128, blank=False)


class Permission(ClassBase):
    class Meta:
        ordering = ("name",)
        verbose_name = "permission"
        verbose_name_plural = "permissions"
        db_table = 'permissions'

    name = models.CharField(max_length=255, blank=False)
    code_name = models.CharField(max_length=255, blank=False)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.code_name

    def is_permission(self, permissions):
        code_names =[]
        for permission in permissions:
            code_names.append(permission['code_name'])

        queryset = self.objects.filter(code_name__in=code_names)
        return queryset


class User(ClassBase, AbstractUser):
    class Meta:
        ordering = ("id",)
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = 'users'

    permissions = models.ManyToManyField(Permission, null=True, blank=True)
    first_name = models.CharField('first name', max_length=150, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    password = models.CharField('password', max_length=128, blank=True)
    email = models.EmailField('email address', blank=False, unique=True)
    groups = models.ManyToManyField(Group, null=True, blank=True)

    def inactivate(self):
        super().is_active = False
        self.is_deleted = True
        self.save()
    
    def __str__(self):
        return self.username
