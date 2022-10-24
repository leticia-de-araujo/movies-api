from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ("Credentials", {"fields": ("username", "email")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birthdate",
                    "bio",
                )
            },
        ),
        ("Permissions", {"fields": ("is_critic",)}),
        ("Dates", {"fields": ("updated_at",)}),
    )


admin.site.register(User, CustomUserAdmin)
