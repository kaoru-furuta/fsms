from django.contrib import admin

from .models import Fruit


class FruitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'created_at', 'updated_at')


admin.site.register(Fruit, FruitAdmin)
