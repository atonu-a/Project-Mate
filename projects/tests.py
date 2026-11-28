from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Project, ProjectMember, Task


class TaskAssignmentTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="password")
        self.member = User.objects.create_user("member", password="password")
        self.other = User.objects.create_user("other", password="password")
        self.project = Project.objects.create(
            owner_name=self.owner,
            title="Test Project",
            desc="Description",
            team_size=3,
            category="Development",
            overview="Overview",
        )
        self.owner_membership = ProjectMember.objects.create(
            project=self.project,
            user=self.owner,
            role="Owner",
        )
        self.member_membership = ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role="Developer",
        )

    def test_owner_can_assign_task_to_project_member(self):
        self.client.login(username="owner", password="password")

        response = self.client.post(
            reverse("task_assign"),
            {
                "project": self.project.pk,
                "member": self.member_membership.pk,
                "title": "Build the feature",
                "desc": "Implement and test it",
                "deadline": "2026-12-15",
            },
        )

        self.assertRedirects(response, reverse("task_view"))
        task = Task.objects.get(title="Build the feature")
        self.assertEqual(task.project, self.project)
        self.assertEqual(task.assigned_to, self.member_membership)
        self.assertEqual(task.assigned_by, self.owner_membership)

    def test_member_from_another_project_cannot_be_assigned(self):
        other_project = Project.objects.create(
            owner_name=self.other,
            title="Other Project",
            desc="Description",
            team_size=2,
            category="Development",
            overview="Overview",
        )
        other_membership = ProjectMember.objects.create(
            project=other_project,
            user=self.other,
            role="Owner",
        )
        self.client.login(username="owner", password="password")

        response = self.client.post(
            reverse("task_assign"),
            {
                "project": self.project.pk,
                "member": other_membership.pk,
                "title": "Invalid assignment",
                "desc": "Should not be created",
                "deadline": "2026-12-15",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Task.objects.filter(title="Invalid assignment").exists())
