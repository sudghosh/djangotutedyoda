from django import forms
from .models import Purchase, Product

class PurchaseForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Product.objects.all(),
                                label='Product',
                                )
    class Meta:
        model = Purchase
        fields = ('name', 'price', 'quantity')
