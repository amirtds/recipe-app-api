from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test user API (Public)"""
    def setUp(self):
        self.client = APIClient()
    # 1. User creation returns 200 status

    def test_create_user_api_success(self):
        # 1.1 define a payload contains email and password
        payload = {
                    'email': 'test@example.com',
                    'password': 'test123',
                    'name': 'Test name'
                    }
        # 1.2 pass payload to create user api and create a user object
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)
        # 1.3 check the sattus is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 1.4 check password doesn't get returned
        self.assertNotIn('password', response.data)
        # 1.5 check password is encryptedd
        self.assertTrue(user.check_password(payload['password']))

    # 2. Extisting user gives 400 bad request
    def test_create_existing_user(self):
        # 2.1 define a payload and create a user based on it
        payload = {
                'email': 'test@example.com',
                'password': 'test123',
                'name': 'Test name'
                }
        create_user(**payload)
        # 2.1 create existing user
        response = self.client.post(CREATE_USER_URL, payload)
        # 2.2 check if status code is 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 3. Too short password not accepted
    def test_create_user_short_password(self):
        # 3.1 define a payload with short password
        payload = {
                'email': 'test@example.com',
                'password': '123',
                'name': 'Test name'
                }
        # 3.2 create a user via api with payload
        response = self.client.post(CREATE_USER_URL, payload)
        # 3.3 if the response status code is 400 because of short password
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 3.4 check if the user didn't get created
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    # 4. Token creation succesful with valid username and password
    def test_token_generation_success(self):
        # 4.1 create a payload, user and pass it to token url
        payload = {'email': 'test@example.com', 'password': 'test123'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)
        # 4.2 check if the status is 200
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        # 4.3 check the token is in response data
        self.assertIn('token', response.data)

    # 5. Token creartion fails if the user doesn't exist
    def test_token_fail_not_existense_user(self):
        # 5.1 create a payload and pass it to token url (user doesn't exist)
        payload = {'email': 'test@example.com', 'password': 'test123'}
        response = self.client.post(TOKEN_URL, payload)
        # 5.2 check if the response is 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 5.3 check response data doesn't contain data
        self.assertNotIn('token', response.data)

    # 6. Token creations fails if username or password is not passed
    def test_token_fail_missing_field(self):
        # 6.1 create token with empt password and pass it to token url
        payload = {'email': 'one', 'password': ''}
        response = self.client.post(TOKEN_URL, payload)
        # 6.2 check we get bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 6.3 check response doesn't have token in it
        self.assertNotIn('token', response.data)

    # 7. test authorization is requiered for user managment
    def test_retrieve_user_unauthorized(self):
        response = self.client.get(ME_URL)
        # 7.1 should get unauthorized if not authenticated
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@londonappdev.com',
            password='testpass',
            name='name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in used"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
