from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """ Test creating new user with valid email """
        email = "test@example.com"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = "test@EXAMPLE.COM"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_without_email(self):
        email = None
        password = "Test123"
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_create_superuser(self):
        email = "test@example.com"
        password = "Test@123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
