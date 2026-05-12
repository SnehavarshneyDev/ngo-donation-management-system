from django.db import models
from registrations.models import Registration
from django.db.models import Q


class Donation(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        SUCCESS = 'S', 'Success'
        FAILED = 'F', 'Failed'
    
    registration=models.ForeignKey(
        Registration,
        on_delete=models.SET_NULL,
        related_name='donations',
        null=True,
    )
    
    amount=models.DecimalField(max_digits=12,decimal_places=2)

    payment_status=models.CharField(max_length=1,choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    payment_provider=models.CharField(max_length=50)

    #Transaction id is only generated once payment is comlpete therefore, it can be blank
    transaction_id=models.CharField(max_length=100,blank=True,null=True)

    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # If transaction id is not null (successfull transaction), allow only unique transaction per provider
            models.UniqueConstraint(
                fields=["transaction_id", "payment_provider"],
                condition=Q(transaction_id__isnull=False) & ~Q(transaction_id=""),
                name="unique_transaction_id_per_provider"
            )
        ]
        indexes = [
            models.Index(fields=["payment_status"]),
            models.Index(fields=["created_at"]),
        ]


    def __str__(self):
        if self.registration:
            return f"{self.registration.user} | {self.amount} | {self.get_payment_status_display()}"
        return f"Deleted registration | {self.amount} | {self.get_payment_status_display()}"

