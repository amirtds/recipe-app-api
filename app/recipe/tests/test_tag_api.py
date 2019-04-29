from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Ingredient

from recipe.serializers import TagSerializer, IngredientSerializer


TAGS_URL = reverse('recipe:tag-list')
INGREDIENTS_URL = reverse("recipe:ingredient-list")


# 1. test that api is not public
class PublicTagApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_api_fail_not_authenticated(self):
        # 1.1 hit the list api
        response = self.client.get(TAGS_URL)
        # 1.2 check if status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):

    def setUp(self):
        # create a user
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="amir@123"
        )
        # create a client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # 2. test that api lists items when user is authenticated
    def test_api_list_success_authenticated(self):
        # 2.1 create couple of tags
        Tag.objects.create(name="test1", user=self.user)
        Tag.objects.create(name="test2", user=self.user)
        # 2.2 hit the list api with authenticated user
        response = self.client.get(TAGS_URL)
        # 2.3 check if the response is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2.4 check if response contains any data
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)

    # 3 check if response contains only user's data
    def test_api_list_limited_to_user(self):
        # 3.1 create another user
        user2 = get_user_model().objects.create_user(
            email="test2@example.com",
            password="test@123"
        )
        # 3.2 create a tag with new user
        tag1 = Tag.objects.create(user=user2, name="tag1")
        # 3.3 create a tag with old user
        tag2 = Tag.objects.create(user=self.user, name="tag2")
        # 3.4 hit API with old user
        response = self.client.get(TAGS_URL)
        # 3.5 check api only contains old user tags
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag2.name)
        self.assertFalse(response.data[0]['name'] == tag1.name)

    # 3. test api creates items if users authenticated
    def test_create_tag_successful(self):
        # 3.1 create a payload contains tags name
        payload = {'name': "test tag"}
        # 3.2 send the payload to tags api
        response = self.client.post(TAGS_URL, payload)
        # 3.3 check the response is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 3.4 check if the tag exist in database
        exists = Tag.objects.filter(
            name=payload['name'],
            user=self.user
            ).exists()
        self.assertTrue(exists)

    # 4. check if tag not get create if payload is empty
    def test_tag_api_fail_missed_field(self):
        paylaod = {"name": ""}
        response = self.client.post(TAGS_URL, paylaod)
        # 4.1 check the repsonse is 400 bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# 5. Test ingredient API - Public
class TestIngredientApiPiblic(TestCase):
    # 5.1 create not authenticated client

    def setUp(self):
        self.client = APIClient()

    def test_api_fail_not_authenticated(self):
        # 5.2 hit the ingredient list endpoint
        response = self.client.get(INGREDIENTS_URL)
        # 5.3 check if the status is unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# 6. Test ingredient API - Private
class TestIngredientApiPrivate(TestCase):
    # 6.1 make setup function to create client and user
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test@123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_api_list_success_authenticated(self):
        # 6.2 hit the ingredient endpoint as authenticated user
        Ingredient.objects.create(
            user=self.user,
            name="test ingredient"
        )
        response = self.client.get(INGREDIENTS_URL)
        # 6.3.1 check if status code is HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 6.3.2 check if there is ingredient in the data
        self.assertEqual(len(response.data), 1)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.data, serializer.data)

    # 6.4 check if user can only see his/her ingredient
    def test_api_list_limited_to_user(self):
        # 6.4.1 create new user
        user2 = get_user_model().objects.create_user(
            email="test2@example.com",
            password="test@123"
        )
        ingredient1 = Ingredient.objects.create(
            user=self.user,
            name="ingredient1"
        )
        # 6.4.2 create new ingredient with new user
        ingredient2 = Ingredient.objects.create(
            user=user2,
            name="ingredient2"
        )
        # 6.4.3 check response only contains user's ingredient
        response = self.client.get(INGREDIENTS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient1.name)
        self.assertFalse(response.data[0]['name'] == ingredient2.name)

    # 6.5 Test ingredient creation endpoint
    def test_create_ingredient_successful(self):
        # 6.5.2 create a payload to contain ingredient
        payload = {'name': 'ingredient1'}
        # 6.5.3 hit the endpoint to create an ingredient
        response = self.client.post(INGREDIENTS_URL, payload)
        # 6.5.4 check if the status is HTTP_201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 6.5.5 check if the response contains the created ingredient
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)

    # 6.6 check creation fails without fields
    def test_ingredient_creation_fails_missing_fields(self):
        payload = {"name": ""}
        response = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
