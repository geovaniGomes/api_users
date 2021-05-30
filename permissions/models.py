from django.db import models


class CustomPermission(models.Model):
    class Meta:
        ordering = ("name",)
        verbose_name = "user_permission"
        verbose_name_plural = "users_permissions"
        db_table = 'permission_custom' 

    name = models.CharField(max_length=255, blank=False, unique=True)
    code_name = models.CharField(max_length=255, blank=False, unique=True)
    is_active = models.BooleanField('active',default=True)

    def __str__(self):
        return self.code_name
