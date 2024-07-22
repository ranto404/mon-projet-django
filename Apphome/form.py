from django import forms
from .models import RATING, ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        widgets = {
            'rating': forms.RadioSelect(choices=RATING),
        }


# class PriceSearchForm(forms.Form):
#     min_price = forms.DecimalField(label='Min Price', required=False, min_value=0)
#     max_price = forms.DecimalField(label='Max Price', required=False, min_value=0)




class PriceSearchForm(forms.Form):
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.HiddenInput())
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre prix',
    }))