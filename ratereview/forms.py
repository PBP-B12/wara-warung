from django import forms
from ratereview.models import UserRateReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserRateReview
        fields = ['rating', 'review']