from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@example.com", password="test123"):
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """ Test the tag string representation """
        # 1. create a tag
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Test Tag"
        )
        # 2. check the tag name is equal to tag str
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ Text representation of the Ingredient """
        # create ingredient and a user
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="test ingredient name"
        )
        # check ingredient name is equal to __str__ ingredient
        self.assertEqual(str(ingredient), ingredient.name)
