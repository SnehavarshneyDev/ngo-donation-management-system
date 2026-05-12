from django.urls import path
from . import views

urlpatterns = [
    path("campaigns/", views.campaign_list, name="campaign_list"),
    path("campaigns/<int:pk>/", views.campaign_detail, name="campaign_detail"),
]
