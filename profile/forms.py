from django import forms
from django.contrib.auth.models import User


class ProfileEditForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="New Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(), required=False, label="Confirm New Password"
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # if email and not User.objects.filter(email=email, id=self.instance.id).exists():
        #     raise forms.ValidationError("A user with that email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "This password is too short. It must contain at least 8 characters."
            )
        return password2
