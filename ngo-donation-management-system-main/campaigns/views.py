from .models import Campaign
from django.shortcuts import render, get_object_or_404
from registrations.models import Registration
from donations.models import Donation

def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, "campaigns/campaign_list.html", {
        "campaigns": campaigns
    })


def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, id=pk)

    is_registered = False
    donation = None

    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user,
            campaign=campaign
        ).exists()

        if is_registered:
            donation = (
                Donation.objects
                .filter(registration__user=request.user,
                        registration__campaign=campaign)
                .order_by("-created_at")
                .first()
            )

    context = {
        "campaign": campaign,
        "is_registered": is_registered,
        "donation": donation,
    }

    return render(request, "campaigns/campaign_detail.html", context)