from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.url = reverse("register")

    def test_register_user_success(self):
        """
        Test successful user registration.
        Checks that:
        - Response status is 201 CREATED
        - Response body is empty {}
        - User is actually created in the database
        """
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "f_user2",
            "last_name": "l_user2",
            "password": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {})
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_password_mismatch(self):
        """
        Test registration failure when passwords do not match.
        Checks that:
        - Response status is 400 BAD REQUEST
        - Error message contains "password"
        """
        data = {
            "username": "user2",
            "email": "user2@example.com",
            "first_name": "f_user2",
            "last_name": "l_user2",
            "password": "password123",
            "password2": "different123",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.json())

    def test_register_user_existing_username(self):
        """
        Test registration failure when username already exists.
        Checks that:
        - Response status is 400 BAD REQUEST
        - Error message contains "username"
        """
        User.objects.create_user(username="existing_user", password="pass12345")
        data = {
            "username": "existing_user",
            "email": "newemail@example.com",
            "first_name": "f_user2",
            "last_name": "l_user2",
            "password": "password123",
            "password2": "password123",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.json())
