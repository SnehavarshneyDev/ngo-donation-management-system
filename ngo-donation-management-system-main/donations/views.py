from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.conf import settings

from registrations.models import Registration
from .models import Donation

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MIN_DONATION_INR = 50  # Stripe minimum (~$0.50)


# =====================================================
# DONATE
# =====================================================
@login_required
def donate(request, campaign_id):
    registration = get_object_or_404(
        Registration,
        user=request.user,
        campaign_id=campaign_id
    )

    campaign = registration.campaign

    # Block only if a payment is currently pending
    pending = Donation.objects.filter(
        registration=registration,
        payment_status=Donation.PaymentStatus.PENDING
    ).first()

    if pending:
        messages.info(
            request,
            "You already have a payment in progress. Please complete it first."
        )
        return redirect("donations:pay", pending.id)

    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Please enter a donation amount.")
            return redirect("donations:donate", campaign.id)

        try:
            amount = int(amount)
        except ValueError:
            messages.error(request, "Invalid donation amount.")
            return redirect("donations:donate", campaign.id)

        if amount < MIN_DONATION_INR:
            messages.error(
                request,
                f"Minimum donation amount is ₹{MIN_DONATION_INR}."
            )
            return redirect("donations:donate", campaign.id)

        donation = Donation.objects.create(
            registration=registration,
            amount=amount,
            payment_status=Donation.PaymentStatus.PENDING,
            payment_provider="stripe_test"
        )

        return redirect("donations:pay", donation.id)

    return render(request, "donations/donate.html", {
        "campaign": campaign,
        "min_amount": MIN_DONATION_INR,
    })


# =====================================================
# PAY (Stripe Checkout)
# =====================================================
@login_required
def pay(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.registration.user != request.user:
        return HttpResponseForbidden("Not allowed")

    if donation.payment_status != Donation.PaymentStatus.PENDING:
        return redirect(
            "campaign_detail",
            donation.registration.campaign.id
        )

    # Safety check (never trust earlier steps blindly)
    if donation.amount < MIN_DONATION_INR:
        messages.error(
            request,
            f"Minimum donation amount is ₹{MIN_DONATION_INR}."
        )
        donation.payment_status = Donation.PaymentStatus.FAILED
        donation.save()
        return redirect(
            "campaign_detail",
            donation.registration.campaign.id
        )

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {
                    "name": donation.registration.campaign.title,
                },
                "unit_amount": int(donation.amount * 100),  # INR → paise
            },
            "quantity": 1,
        }],
        success_url=request.build_absolute_uri(
            reverse("donations:stripe_success", args=[donation.id])
        ),
        cancel_url=request.build_absolute_uri(
            reverse("donations:stripe_cancel", args=[donation.id])
        ),
    )

    return redirect(session.url)


# =====================================================
# STRIPE SUCCESS
# =====================================================
@login_required
def stripe_success(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.registration.user != request.user:
        return HttpResponseForbidden("Not allowed")

    if donation.payment_status != Donation.PaymentStatus.PENDING:
        return redirect(
            "campaign_detail",
            donation.registration.campaign.id
        )

    donation.payment_status = Donation.PaymentStatus.SUCCESS
    donation.save()

    return render(request, "donations/success.html", {
        "donation": donation
    })


# =====================================================
# STRIPE CANCEL / FAILURE
# =====================================================
@login_required
def stripe_cancel(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)

    if donation.registration.user != request.user:
        return HttpResponseForbidden("Not allowed")

    if donation.payment_status != Donation.PaymentStatus.PENDING:
        return redirect(
            "campaign_detail",
            donation.registration.campaign.id
        )

    donation.payment_status = Donation.PaymentStatus.FAILED
    donation.save()

    return render(request, "donations/failed.html", {
        "donation": donation
    })
