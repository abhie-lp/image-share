from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name", "email"


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "date_of_birth", "photo"


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = "username", "first_name", "last_name", "email"
        
    def clean_repeat_password(self):
        cd = self.cleaned_data
        if cd["password"] != cd["repeat_password"]:
            raise forms.ValidationError("Passwords don't match.")
        return cd["repeat_password"]
