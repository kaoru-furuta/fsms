from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ["username", "is_staff"]
    readonly_fields = ("is_staff",)


admin.site.register(User, UserAdmin)
