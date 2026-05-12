from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "registration_name",
        "registration_user",
        "registration_campaign",
        "amount",
        "payment_status",
        "payment_provider",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "payment_provider",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "registration__name",
        "registration__user__username",
        "registration__user__email",
        "transaction_id",
    )

    raw_id_fields = (
        "registration",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "registration",
        "amount",
        "payment_status",
        "payment_provider",
        "transaction_id",
        "created_at",
    )

    actions = ("export_donations_csv",)

    fieldsets = (
        ("Payment Info", {
            "fields": (
                "amount",
                "payment_status",
                "payment_provider",
                "transaction_id",
            )
        }),
        ("Registration Info", {
            "fields": ("registration",)
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    # ---------- display helpers ----------

    def registration_name(self, obj):
        return obj.registration.name if obj.registration else "-"
    registration_name.short_description = "Name"

    def registration_user(self, obj):
        return obj.registration.user if obj.registration else "-"
    registration_user.short_description = "User"

    def registration_campaign(self, obj):
        return obj.registration.campaign if obj.registration else "-"
    registration_campaign.short_description = "Campaign"

    # ---------- CSV EXPORT ACTION ----------

    def export_donations_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="donations_export.csv"'

        writer = csv.writer(response)

        # CSV header
        writer.writerow([
            "Donation ID",
            "Amount",
            "Payment Status",
            "Payment Provider",
            "Transaction ID",
            "Donation Created At",

            "Registration Name",
            "Registration Created At",

            "Campaign Title",

            "User ID",
            "Username",
            "User Email",
        ])

        # Optimize queries
        queryset = queryset.select_related(
            "registration",
            "registration__user",
            "registration__campaign",
        )

        for donation in queryset:
            registration = donation.registration
            user = registration.user if registration else None
            campaign = registration.campaign if registration else None

            writer.writerow([
                donation.id,
                donation.amount,
                donation.get_payment_status_display(),
                donation.payment_provider,
                donation.transaction_id,
                donation.created_at,

                registration.name if registration else "",
                registration.created_at if registration else "",

                campaign.title if campaign else "",

                user.id if user else "",
                user.username if user else "",
                user.email if user else "",
            ])

        return response

    export_donations_csv.short_description = "Export selected donations as CSV"