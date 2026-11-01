from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from .push import send_push_notification


@receiver(post_save, sender=Notification, dispatch_uid="send_notification_push")
def send_notification_push(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(
            lambda: send_push_notification(instance)
        )
