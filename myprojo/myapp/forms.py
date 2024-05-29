from django import forms
from .models import Cart

class CartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1)  # Add quantity field here

    class Meta:
        model = Cart
        fields = ['quantity']  # Include 'quantity' field in fields list 