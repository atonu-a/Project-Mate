import json
import logging

from django.conf import settings
from firebase_admin import credentials, exceptions, get_app, initialize_app, messaging
from google.auth.exceptions import DefaultCredentialsError

from .models import FirebaseInstallation


logger = logging.getLogger(__name__)


def _firebase_app():
    try:
        return get_app()
    except ValueError:
        pass

    service_account_json = settings.FIREBASE_SERVICE_ACCOUNT_JSON
    try:
        if service_account_json:
            service_account = json.loads(service_account_json)
            credential = credentials.Certificate(service_account)
        else:
            credential = credentials.ApplicationDefault()
        return initialize_app(credential)
    except (DefaultCredentialsError, exceptions.FirebaseError, ValueError):
        logger.exception("Could not initialize Firebase Admin SDK")
        return None


def send_push_notification(notification):
    devices = list(
        FirebaseInstallation.objects.filter(user=notification.recipient)
    )
    if not devices:
        return

    app = _firebase_app()
    if app is None:
        return

    payload = {
        "title": notification.get_notification_type_display(),
        "body": notification.content,
        "url": notification.target_url,
    }

    for device in devices:
        try:
            message = messaging.Message(data=payload, token=device.fcm_token)
            messaging.send(message, app=app)
        except messaging.UnregisteredError:
            logger.info("Removing expired FCM token for user %s", device.user.pk)
            device.delete()
        except ValueError:
            logger.exception(
                "Removing invalid FCM token for user %s",
                device.user.pk,
            )
            device.delete()
        except (DefaultCredentialsError, exceptions.FirebaseError):
            logger.exception(
                "Could not send push notification %s to user %s",
                notification.pk,
                device.user.pk,
            )
