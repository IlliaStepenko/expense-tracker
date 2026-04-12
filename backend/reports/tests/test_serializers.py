from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import TestCase
from reports.models import ExpenseReport
from reports.serializers import (
    ExpenseReportDetailSerializer,
    ExpenseReportListSerializer,
    ExpenseReportMarkViewedSerializer,
)

User = get_user_model()


class ExpenseReportSerializersTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        now = datetime.now()

        self.report = ExpenseReport.objects.create(
            user=self.user,
            date_from=now - timedelta(days=10),
            date_to=now - timedelta(days=5),
            result={"sum": 100},
            report_type="weekly",
            is_viewed=False,
        )

    def test_list_serializer_fields(self):
        serializer = ExpenseReportListSerializer(self.report)
        self.assertEqual(
            set(serializer.data.keys()),
            {"id", "created_at", "report_type", "is_viewed"},
        )

    def test_list_serializer_values(self):
        serializer = ExpenseReportListSerializer(self.report)
        self.assertEqual(serializer.data["id"], str(self.report.id))
        self.assertEqual(serializer.data["report_type"], self.report.report_type)
        self.assertEqual(serializer.data["is_viewed"], self.report.is_viewed)

    def test_mark_viewed_serializer_valid(self):
        data = {"id": str(uuid4())}
        serializer = ExpenseReportMarkViewedSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_mark_viewed_serializer_invalid_uuid(self):
        data = {"id": "not-a-uuid"}
        serializer = ExpenseReportMarkViewedSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_detail_serializer_fields(self):
        serializer = ExpenseReportDetailSerializer(self.report)
        self.assertEqual(
            set(serializer.data.keys()),
            {
                "id",
                "date_from",
                "date_to",
                "result",
                "is_viewed",
                "report_type",
                "created_at",
            },
        )

    def test_detail_serializer_values(self):
        serializer = ExpenseReportDetailSerializer(self.report)
        self.assertEqual(serializer.data["id"], str(self.report.id))
        self.assertEqual(serializer.data["report_type"], self.report.report_type)
        self.assertEqual(serializer.data["is_viewed"], self.report.is_viewed)
        self.assertEqual(serializer.data["result"], self.report.result)
