from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
User = get_user_model()

from accountProfile.models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **Kwargs):
    if created:
        Profile.objects.create(user=instance)
