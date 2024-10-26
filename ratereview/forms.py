from django import forms
from .models import UserRateReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserRateReview
        fields = ['rate', 'review']