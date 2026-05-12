from django.contrib import admin
from django.db.models import Sum
from .models import Campaign
from donations.models import Donation


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "goal_amount",
        "total_donations",
        "start_date",
        "end_date",
        "is_active",
    )

    readonly_fields = ("created_at", "total_donations")

    # -----------------------------
    # Per-campaign total donation
    # -----------------------------
    def total_donations(self, obj):
        return (
            Donation.objects
            .filter(
                registration__campaign=obj,
                payment_status=Donation.PaymentStatus.SUCCESS, 
            )
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )

    total_donations.short_description = "Total Donations (₹)"

    # -----------------------------
    # Overall donation (all campaigns)
    # -----------------------------
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        overall_total = (
            Donation.objects
            .filter(payment_status=Donation.PaymentStatus.SUCCESS) 
            .aggregate(total=Sum("amount"))["total"]
        )

        extra_context["overall_donation_amount"] = overall_total or 0
        return super().changelist_view(request, extra_context=extra_context)