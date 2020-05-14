import unicodedata

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

        # Mac 環境などでファイル名が NFD になっていることがあるので NFC に変換しておく
        data.name = unicodedata.normalize("NFC", data.name)

        if Fruit.objects.filter(image=data.name).exists():
            raise forms.ValidationError("ファイル名が重複しています。")

        return data

    class Meta:
        model = Fruit
        fields = ("name", "price", "image")


class SearchForm(forms.Form):
    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
