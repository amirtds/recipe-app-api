from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    """" Test Admin site """
    def setUp(self):
        # 1. create a test user
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="Test123",
            name="Test user full name"
        )
        # 2. create test super user
        self.superuser = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="Test123"
        )
        # 3. establish a client
        self.client = Client()
        # 4 Login admin user to admin site
        self.client.force_login(self.superuser)

    def test_users_listed(self):
        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_create_page(self):
        url = reverse("admin:core_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
