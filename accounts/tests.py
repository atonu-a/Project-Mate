from unittest.mock import patch

from django.test import SimpleTestCase

from .models import Profile


class ProfilePictureUrlTests(SimpleTestCase):
    def test_default_profile_picture_uses_unversioned_cloudinary_url(self):
        profile = Profile(profile_pic="default_mdzqdy.svg")

        self.assertEqual(
            profile.profile_pic_url,
            "https://res.cloudinary.com/ddrochzoq/image/upload/default_mdzqdy.svg",
        )

    def test_missing_profile_picture_uses_unversioned_cloudinary_url(self):
        profile = Profile(profile_pic=None)

        self.assertEqual(
            profile.profile_pic_url,
            "https://res.cloudinary.com/ddrochzoq/image/upload/default_mdzqdy.svg",
        )

    def test_uploaded_profile_picture_uses_storage_url(self):
        profile = Profile(profile_pic="images/avatar.jpg")
        storage = profile.profile_pic.storage

        with patch.object(storage, "url", return_value="https://cloudinary.test/avatar.jpg") as url:
            self.assertEqual(
                profile.profile_pic_url,
                "https://cloudinary.test/avatar.jpg",
            )

        url.assert_called_once_with("images/avatar.jpg")
