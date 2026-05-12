from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # what is shown in the users list page
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )

    # filters on the right sidebar
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "groups",
    )

    # search box
    search_fields = (
        "username",
        "email",
    )

    ordering = (
        "username",
    )

    # fields shown while editing an existing user
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ("Personal info", {
            "fields": ("email", "first_name", "last_name")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    # fields shown while creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )
