from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from reports.models import ExpenseReport
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class ExpenseReportMarkViewedAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user1", password="pass123")
        self.other_user = User.objects.create_user(username="user2", password="pass123")

        now = datetime.now()

        self.report = ExpenseReport.objects.create(
            user=self.user,
            date_from=now - timedelta(days=10),
            date_to=now - timedelta(days=5),
            result={"sum": 100},
            report_type="weekly",
            is_viewed=False,
        )

    def test_auth_required(self):
        url = reverse("expense_report_mark_viewed", args=[self.report.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_viewed_success(self):
        self.client.force_authenticate(self.user)
        url = reverse("expense_report_mark_viewed", args=[self.report.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.report.refresh_from_db()
        self.assertTrue(self.report.is_viewed)

        self.assertEqual(response.data["id"], str(self.report.id))
        self.assertEqual(response.data["is_viewed"], True)

    def test_mark_viewed_when_already_viewed(self):
        self.report.is_viewed = True
        self.report.save()

        self.client.force_authenticate(self.user)
        url = reverse("expense_report_mark_viewed", args=[self.report.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.report.refresh_from_db()
        self.assertTrue(self.report.is_viewed)

    def test_mark_viewed_other_user_report(self):
        self.client.force_authenticate(self.other_user)
        url = reverse("expense_report_mark_viewed", args=[self.report.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Report not found.")

    def test_mark_viewed_invalid_id(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "expense_report_mark_viewed", args=["00000000-0000-0000-0000-000000000000"]
        )

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
