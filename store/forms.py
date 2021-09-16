from django import forms
from django.forms import fields

from store.models import Review

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('__all__')
        