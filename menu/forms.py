from django.forms import ModelForm
from menu.models import Menu
from django.utils.html import strip_tags
from django import forms
from warung.models import Warung

class MenuForm(ModelForm):
    warung = forms.ModelChoiceField(queryset=Warung.objects.all(), label="Select Warung")
    class Meta:
        model = Menu
        fields = ['warung', 'menu', 'harga', 'gambar']