from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UsercreateForm
from core.models import User, Group, Permission

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UsercreateForm


admin.site.register(Group)
admin.site.register(Permission)

