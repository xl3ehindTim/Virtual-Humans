from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
