from django import forms
from django.utils import timezone

from fruits.models import Fruit

from .models import Sale

forms.DateTimeInput.input_type = "datetime-local"


def get_fruit_list():
    return [(fruit.id, fruit.name) for fruit in Fruit.objects.all()]


class SaleForm(forms.ModelForm):
    fruit_list = forms.ChoiceField(
        choices=get_fruit_list, widget=forms.Select(attrs={"class": "form-control"})
    )
    number = forms.IntegerField(
        min_value=1, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    sold_at = forms.DateTimeField(
        initial=timezone.now,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Sale
        fields = ("fruit_list", "number", "sold_at")


class UploadFileForm(forms.Form):
    file = forms.FileField()
