from django import forms
from user_dashboard.models import UserEntry
from django.contrib.auth.models import User

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserEntry
        fields = ['email', 'phone_number', 'address', 'date_of_birth']

class EditUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
