from django.contrib.auth.forms import UserCreationForm

from .models import User
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password", 'name')


class UploadAvatar(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar",)


