from datetime import datetime
from os.path import splitext

from django import forms

from .models import Fruit


class FruitForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    image = forms.FileField(
        required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    def clean_image(self):
        data = self.cleaned_data["image"]

        if not data:
            return data

        # ファイル名が重複しないように現在時刻を追加
        basename, ext = splitext(data.name)
        data.name = f"{basename}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"

        return data

    class Meta:
        model = Fruit
        fields = ("name", "price", "image")


class SearchForm(forms.Form):
    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
