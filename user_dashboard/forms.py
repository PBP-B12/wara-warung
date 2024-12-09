from django import forms
from .models import UserEntry
from django.contrib.auth.models import User

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserEntry
        fields = ['email', 'phone_number', 'address', 'date_of_birth']
