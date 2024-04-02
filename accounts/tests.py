import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

USER_LIST_URL = reverse("accounts:profiles")


def image_upload_url(user_id):
    return reverse("accounts:me", args=[user_id])


class UserProfilePictureUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.user.profile_picture.delete()

    def test_upload_profile_picture(self):
        """Test uploading an image to movie"""
        url = image_upload_url(self.user.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.patch(url, {"profile_picture": ntf}, format="multipart")
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("profile_picture", res.data)
        self.assertTrue(os.path.exists(self.user.profile_picture.path))

    def test_upload_picture_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.user.id)
        res = self.client.patch(url, {"profile_picture": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_url_is_shown_on_airplane_list(self):
        url = image_upload_url(self.user.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.patch(url, {"profile_picture": ntf}, format="multipart")
        res = self.client.get(USER_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("profile_picture", res.data[0].keys())


class UnauthorizedTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )

    def test_auth_required(self):
        url = image_upload_url(1)
        response = self.client.patch(url, {"profile_picture": "not image"}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "testpassword123"
        )
        self.target_user = get_user_model().objects.create_user(
            "target@test.com", "targetpassword123"
        )

    def test_follow_unfollow_user(self):
        follow_url = reverse("accounts:follow")
        res = self.client.post(
            follow_url,
            {"user_id": self.target_user.id}
        )
        follow_instance = self.user.follower.first()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(follow_instance.following, self.target_user)
        self.assertEqual(follow_instance.follower, self.user)

        unfollow_url = reverse("accounts:unfollow")
        res = self.client.post(
            unfollow_url,
            {"user_id": self.target_user.id}
        )
        follow_instance = self.user.follower.first()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(follow_instance, None)
