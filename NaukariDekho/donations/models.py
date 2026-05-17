from django.db import models

from django.utils import timezone

from datetime import timedelta


class Donation(models.Model):

    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    qr_code = models.ImageField(
        upload_to='donation_qr/',
        blank=True,
        null=True
    )

    is_paid = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):

        if not self.expires_at:

            self.expires_at = timezone.now() + timedelta(minutes=5)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.first_name