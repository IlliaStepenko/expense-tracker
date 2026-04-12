import uuid
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from export.models import ExportResult
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ExportResultTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    @patch("export.views.generate_export.delay")
    def test_create_export_result(self, mock_generate_export):
        url = reverse("create_export")
        data = {}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        export_result = ExportResult.objects.get(user=self.user)
        mock_generate_export.assert_called_once_with(str(export_result.id))
        self.assertIn("export_result_id", response.data)
        self.assertIn("status", response.data)

    def test_get_export_result_detail(self):
        export_result = ExportResult.objects.create(
            user=self.user,
            status="pending",
        )
        url = reverse(
            "export_detail", kwargs={"export_result_id": str(export_result.id)}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(export_result.id))
        self.assertEqual(response.data["status"], export_result.status)

    def test_get_export_result_detail_not_found(self):
        random_uuid = uuid.uuid4()
        url = reverse("export_detail", kwargs={"export_result_id": str(random_uuid)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
