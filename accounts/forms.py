from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        error_messages={"invalid": "Enter a valid email address"},
    )
    first_name = forms.CharField(max_length=120, required=False)  # Optional
    last_name = forms.CharField(max_length=120, required=False)  # Optional

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        # If the email is not required, it can be empty
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match")
        if len(password1) < 8:
            raise ValidationError(
                "This password is too short. It must contain at least 8 characters"
            )
        return password2
