from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from export.models import ExportResult
from export.serializers import (
    ExportResultCreateSerializer,
    ExportResultSerializer,
    ExportResultSimpleResponseSerializer,
)
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ExportResultSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_export_result_serializer_success_with_file(self):
        mock_file = MagicMock()
        mock_file.url = "/media/test.csv"
        export_result = ExportResult(
            id="12345678-1234-5678-1234-567812345678",
            user=self.user,
            status="SUCCESS",
            file_path=mock_file,
        )
        request = MagicMock()
        request.build_absolute_uri.return_value = "http://testserver/media/test.csv"

        serializer = ExportResultSerializer(export_result, context={"request": request})
        data = serializer.data

        self.assertEqual(data["id"], str(export_result.id))
        self.assertEqual(data["status"], export_result.status)
        self.assertEqual(data["download_url"], "http://testserver/media/test.csv")

    def test_export_result_serializer_pending_without_file(self):
        export_result = ExportResult(
            id="12345678-1234-5678-1234-567812345679",
            user=self.user,
            status="PENDING",
            file_path=None,
        )
        serializer = ExportResultSerializer(
            export_result, context={"request": MagicMock()}
        )
        data = serializer.data
        self.assertIsNone(data["download_url"])


class ExportResultCreateSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.factory = MagicMock()
        self.factory.user = self.user

    def test_create_export_result_with_params(self):
        data = {"params": {"foo": "bar"}}
        serializer = ExportResultCreateSerializer(
            data=data, context={"request": self.factory}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        export_result = serializer.save()

        self.assertEqual(export_result.user, self.user)
        self.assertEqual(export_result.params, {"foo": "bar"})
        self.assertEqual(export_result.status, "PENDING")
        self.assertEqual(export_result.format, "csv")

    def test_create_export_result_without_params(self):
        serializer = ExportResultCreateSerializer(
            data={}, context={"request": self.factory}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        export_result = serializer.save()

        self.assertEqual(export_result.params, {})
        self.assertEqual(export_result.status, "PENDING")


class ExportResultSimpleResponseSerializerTests(TestCase):

    def test_simple_response_serializer_valid(self):
        data = {
            "export_result_id": "12345678-1234-5678-1234-567812345678",
            "status": "PENDING",
        }
        serializer = ExportResultSimpleResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(
            str(serializer.validated_data["export_result_id"]), data["export_result_id"]
        )
        self.assertEqual(serializer.validated_data["status"], data["status"])

    def test_simple_response_serializer_invalid_uuid(self):
        data = {"export_result_id": "not-a-uuid", "status": "PENDING"}
        serializer = ExportResultSimpleResponseSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
