from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):

    # CREATE PROFILE when user is created
    if created:
        Profile.objects.create(user=instance)

    # UPDATE PROFILE safely
    else:
        # prevents crash if profile somehow missing
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()