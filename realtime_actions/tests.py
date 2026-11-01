from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Notification


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="notice-user",
            password="test-pass",
        )
        self.client.force_login(self.user)
        self.notification = Notification.objects.create(
            recipient=self.user,
            notification_type=Notification.NotificationType.PROJECT_COMMENT,
            content="A teammate commented on your project",
            target_url="/notifications/",
        )

    def test_notifications_page_shows_current_users_notifications(self):
        response = self.client.get(reverse("notifications"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.notification.content)

    def test_mark_all_as_read(self):
        response = self.client.post(reverse("mark_as_read"))

        self.assertRedirects(response, reverse("notifications"))
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
