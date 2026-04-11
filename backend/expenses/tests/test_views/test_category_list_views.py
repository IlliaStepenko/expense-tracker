from django.contrib.auth import get_user_model
from django.urls import reverse
from expenses.models import Category
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CategoryListViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")

        self.default_category = Category.objects.create(
            name="Groceries", is_default=True
        )
        self.user1_category = Category.objects.create(
            name="User1 Transport", is_default=False, user=self.user1
        )
        self.user2_category = Category.objects.create(
            name="User2 Health", is_default=False, user=self.user2
        )

        self.url = reverse("expenses:category_list")

        refresh = RefreshToken.for_user(self.user1)
        self.jwt_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")

    def test_list_categories_authenticated_user(self):
        """Check that an authenticated user sees default and their own categories"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_names = [cat["name"] for cat in response.data]
        self.assertIn(self.default_category.name, category_names)
        self.assertIn(self.user1_category.name, category_names)
        self.assertNotIn(self.user2_category.name, category_names)

    def test_list_categories_unauthenticated_user(self):
        """Unauthenticated users should not get the list"""
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
