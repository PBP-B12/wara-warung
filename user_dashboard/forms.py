from django import forms
from .models import UserDashboard

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserDashboard
        fields = ['email', 'phone_number', 'address', 'date_of_birth', 'budget']
