from django.contrib import admin

from .models import Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'fruit', 'number', 'amount', 'sold_at')


admin.site.register(Sale, SaleAdmin)
