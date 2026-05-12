from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "campaign",
        "created_at",
    )

    list_filter = (
        "campaign",
        "created_at",
    )

    search_fields = (
        "name",
        "user__username",
        "user__email",
    )

    raw_id_fields = (
        "user",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "name",
        "user",
    )

    fieldsets = (
        ("Registration Info", {
            "fields": ("user", "name")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )
