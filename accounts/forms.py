from . import models
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = "username", "first_name", "email",
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password2"] != cd["password"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["password2"]


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "first_name", "last_name", "email",


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = "date_of_birth", "photo",
        widgets = {"date_of_birth": forms.DateInput}
