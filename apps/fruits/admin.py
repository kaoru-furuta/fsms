from django import forms
from django.contrib import admin

from .models import Fruit


class FruitAdminForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput)

    class Meta:
        model = Fruit
        fields = "__all__"


class FruitAdmin(admin.ModelAdmin):
    form = FruitAdminForm


admin.site.register(Fruit, FruitAdmin)
