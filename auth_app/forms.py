from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import Profile
from django.utils.html import strip_tags

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_user(self):
        username = self.cleaned_data['username']
        return strip_tags(username)