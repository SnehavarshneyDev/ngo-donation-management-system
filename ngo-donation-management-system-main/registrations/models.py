from django.db import models
from campaigns.models import Campaign
# We don't directly import default django auth user to avoid hard coding django-user
from django.conf import settings 


class Registration(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Registration cannot exist without user
        related_name="registrations"
    )
    
    name=models.CharField(max_length=255,blank=True) # Allowing anonymous registrations

    created_at=models.DateTimeField(auto_now_add=True)

    campaign=models.ForeignKey(
        Campaign, 
        on_delete=models.PROTECT,
        related_name="registrations",
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "campaign"],
                name="unique_user_campaign"
            ),
        ]
    
    def __str__(self):
        return f"{self.user} → {self.campaign}"
