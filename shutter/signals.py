from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save

from .models import Profile, Album


def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)


def update_profile(sender, instance, created, *args, **kwargs):
    if not created:
        instance.profile.save()


post_save.connect(create_profile, sender=User)


