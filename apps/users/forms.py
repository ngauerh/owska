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


class RequiredFieldsMixin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_required = getattr(self.Meta, 'fields_required', None)
        if fields_required:
            for key in self.fields:
                self.fields[key].required = False


class DetailsForm(RequiredFieldsMixin):
    class Meta:
        model = User
        fields = ["website", "company", "location", "weibo", "twitter", "github", "instagram", "telegram", "linkedin",
                  "biography"]
        fields_required = ["website", "company", "location", "weibo", "twitter", "github", "instagram", "telegram", "linkedin",
                  "biography"]



