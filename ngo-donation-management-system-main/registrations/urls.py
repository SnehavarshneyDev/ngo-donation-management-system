from django.urls import path
from . import views

urlpatterns = [
    path(
        "campaign/<int:campaign_id>/register/",
        views.register_for_campaign,
        name="campaign_register"
    ),
]
