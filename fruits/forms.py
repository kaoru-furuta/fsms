from django import forms

from .models import Fruit


class FruitForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Fruit
        fields = ("name", "price")
