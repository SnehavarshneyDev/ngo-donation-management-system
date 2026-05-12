from django.urls import path
from . import views

app_name = "donations"

urlpatterns = [
    path("donate/<int:campaign_id>/", views.donate, name="donate"),
    path("pay/<int:donation_id>/", views.pay, name="pay"),
    path("stripe/success/<int:donation_id>/", views.stripe_success, name="stripe_success"),
    path("stripe/cancel/<int:donation_id>/", views.stripe_cancel, name="stripe_cancel"),
]
