from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from campaigns.models import Campaign

def home(request):
    campaigns = Campaign.objects.filter(is_active=True)
    return render(request, "home.html", {
        "campaigns": campaigns
    })

def about(request):
    return render(request, "pages/about.html")

def contact(request):
    return render(request, "pages/contact.html")
