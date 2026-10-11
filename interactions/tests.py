from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Follow


class ToggleFollowTests(TestCase):
    def test_following_admin_account_redirects_to_its_profile(self):
        follower = User.objects.create_user(username="follower", password="test")
        admin_user = User.objects.create_user(username="admin", password="test")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        self.client.force_login(follower)

        response = self.client.post(
            reverse("follow", kwargs={"username": admin_user.username}),
            HTTP_REFERER="/admin/",
        )

        self.assertRedirects(
            response,
            reverse("public_profile", kwargs={"username": admin_user.username}),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            Follow.objects.filter(follower=follower, following=admin_user).exists()
        )
