from django.urls import path
from .views import CustomLoginView, profile, signup

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
]
