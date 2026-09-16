from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from core.forms import BootstrapFormMixin


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="Email", required=False, help_text="Необязательно.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass
