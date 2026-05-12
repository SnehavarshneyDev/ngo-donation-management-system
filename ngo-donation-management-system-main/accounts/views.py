from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from registrations.models import Registration
from donations.models import Donation


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return reverse_lazy("admin:index")   # Django admin dashboard
        return reverse_lazy("profile")           # User profile page


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # New users are never admins → send directly to profile
            return redirect("profile")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    user = request.user

    registrations = (
        Registration.objects
        .filter(user=user)
        .select_related("campaign")
        .order_by("-created_at")
    )

    donations = (
        Donation.objects
        .filter(registration__user=user)
        .select_related("registration", "registration__campaign")
        .order_by("-created_at")
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "user_obj": user,
            "registrations": registrations,
            "donations": donations,
        }
    )
