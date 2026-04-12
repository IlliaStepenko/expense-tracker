from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from reports.models import ExpenseReport
from reports.serializers import (
    ExpenseReportDetailSerializer,
    ExpenseReportListSerializer,
)
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class ExpenseReportViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user1", password="pass123")
        self.other_user = User.objects.create_user(username="user2", password="pass123")

        now = datetime.now()

        self.r1 = ExpenseReport.objects.create(
            user=self.user,
            date_from=now - timedelta(days=10),
            date_to=now - timedelta(days=5),
            result={"sum": 100},
            report_type="weekly",
        )
        self.r2 = ExpenseReport.objects.create(
            user=self.other_user,
            date_from=now - timedelta(days=20),
            date_to=now - timedelta(days=15),
            result={"sum": 200},
            report_type="monthly",
        )

    def test_auth_required(self):
        url = reverse("expense_report-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset_returns_only_user_reports(self):
        self.client.force_authenticate(self.user)
        url = reverse("expense_report-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in response.data}
        self.assertEqual(ids, {str(self.r1.id)})

    def test_get_serializer_class_list(self):
        self.client.force_authenticate(self.user)
        url = reverse("expense_report-list")

        response = self.client.get(url)

        serializer = ExpenseReportListSerializer([self.r1], many=True)
        self.assertEqual(set(response.data[0].keys()), set(serializer.data[0].keys()))

    def test_get_serializer_class_detail(self):
        self.client.force_authenticate(self.user)
        url = reverse("expense_report-detail", args=[self.r1.id])

        response = self.client.get(url)

        serializer = ExpenseReportDetailSerializer(self.r1)
        self.assertEqual(set(response.data.keys()), set(serializer.data.keys()))
