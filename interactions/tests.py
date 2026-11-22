from datetime import timedelta

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Comment, Follow
from .utils import attach_comment_tree


class CommentTreeTests(SimpleTestCase):
    def test_attaches_replies_at_multiple_depths(self):
        project = type("ProjectStub", (), {})()
        root = Comment(id=1, parent_id=None, created_at=timezone.now())
        reply = Comment(id=2, parent_id=1, created_at=timezone.now())
        nested_reply = Comment(id=3, parent_id=2, created_at=timezone.now())
        project.all_comments = [root, reply, nested_reply]

        attach_comment_tree(project)

        self.assertEqual(project.prefetched_comments, [root])
        self.assertEqual(root.prefetched_replies, [reply])
        self.assertEqual(reply.prefetched_replies, [nested_reply])
        self.assertEqual(nested_reply.prefetched_replies, [])


class CommentTimestampTests(TestCase):
    def test_reply_exposes_created_at_ago(self):
        reply = Comment(
            parent_id=1,
            created_at=timezone.now() - timedelta(minutes=5),
        )

        self.assertEqual(reply.created_at_ago, "5m ago")


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
