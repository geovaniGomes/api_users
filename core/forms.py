from django.contrib.auth import forms

from core.models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User
        fields = "__all__"


class UsercreateForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm):
        model = User
        fields = "__all__"