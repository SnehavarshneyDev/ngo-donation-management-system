from django.db import models

class Campaign(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.BigIntegerField(blank=True, null=True)

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to="campaigns/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["start_date"]),
        ]

    def __str__(self):
        return self.title
