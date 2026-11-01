import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from firebase_admin import messaging

from .models import FirebaseInstallation, Notification
from .push import send_push_notification, send_test_push


class FirebaseTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="push-user",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.url = reverse("save_firebase_token")

    @patch("realtime_actions.views.send_test_push", return_value=None)
    def test_saves_fcm_token_for_authenticated_user(self, send_test_push):
        response = self.client.post(
            self.url,
            data=json.dumps({"fcm_token": "browser-fcm-token"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            FirebaseInstallation.objects.filter(
                user=self.user,
                fcm_token="browser-fcm-token",
            ).exists()
        )
        send_test_push.assert_called_once_with("browser-fcm-token")

    @patch(
        "realtime_actions.views.send_test_push",
        return_value="Push messaging is not configured on the server.",
    )
    def test_reports_when_push_delivery_is_not_configured(self, _send_test_push):
        response = self.client.post(
            self.url,
            data=json.dumps({"fcm_token": "browser-fcm-token"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn("not configured", response.json()["error"])
        self.assertTrue(
            FirebaseInstallation.objects.filter(
                user=self.user,
                fcm_token="browser-fcm-token",
            ).exists()
        )

    def test_rejects_missing_or_invalid_token(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"fcm_token": ["not", "a", "token"]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FirebaseInstallation.objects.count(), 0)

    def test_serves_firebase_service_worker_from_site_root(self):
        response = self.client.get(
            reverse("firebase_messaging_service_worker")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertEqual(response["Cache-Control"], "no-cache")
        self.assertIn(
            b"firebase.messaging()",
            b"".join(response.streaming_content),
        )


class NotificationPushSignalTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="notice-user",
            password="test-password",
        )

    @patch("realtime_actions.signals.send_push_notification")
    def test_new_notification_sends_push_after_commit(self, send_push):
        notification = Notification.objects.create(
            recipient=self.user,
            notification_type=Notification.NotificationType.NEW_FOLLOWER,
            content="Someone followed you",
            target_url="/notifications/",
        )

        send_push.assert_called_once_with(notification)


class PushDeliveryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="push-recipient",
            password="test-password",
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type=Notification.NotificationType.PROJECT_COMMENT,
            content="A teammate commented on your project",
            target_url="/notifications/",
        )
        FirebaseInstallation.objects.create(
            user=self.user,
            fcm_token="browser-fcm-token",
        )

    @patch("realtime_actions.push.messaging.send")
    @patch("realtime_actions.push._firebase_app", return_value=object())
    def test_sends_notification_data_to_saved_token(self, firebase_app_mock, send):
        send_push_notification(self.notification)

        firebase_app_mock.assert_called_once_with()
        message = send.call_args.args[0]
        self.assertEqual(message.token, "browser-fcm-token")
        self.assertEqual(
            message.data,
            {
                "title": "Project Comment",
                "body": "A teammate commented on your project",
                "url": "/notifications/",
            },
        )

    @patch(
        "realtime_actions.push.messaging.send",
        side_effect=messaging.UnregisteredError("token expired"),
    )
    @patch("realtime_actions.push._firebase_app", return_value=object())
    def test_removes_expired_token(self, _firebase_app_mock, _send):
        send_push_notification(self.notification)

        _firebase_app_mock.assert_called_once_with()
        _send.assert_called_once()
        self.assertFalse(
            FirebaseInstallation.objects.filter(
                fcm_token="browser-fcm-token"
            ).exists()
        )

    @patch("realtime_actions.push.messaging.send", return_value="message-id")
    @patch("realtime_actions.push._firebase_app", return_value=object())
    def test_sends_test_notification_to_registered_browser(
        self,
        _firebase_app_mock,
        send,
    ):
        result = send_test_push("browser-fcm-token")

        self.assertIsNone(result)
        message = send.call_args.args[0]
        self.assertEqual(message.token, "browser-fcm-token")
        self.assertEqual(message.data["title"], "ProjectMate test notification")

    @patch("realtime_actions.push._firebase_app", return_value=None)
    def test_reports_missing_firebase_server_credentials(self, _firebase_app_mock):
        result = send_test_push("browser-fcm-token")

        self.assertIn("FIREBASE_SERVICE_ACCOUNT_JSON", result)
