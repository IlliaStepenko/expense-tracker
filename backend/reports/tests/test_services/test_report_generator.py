from datetime import timedelta
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from reports.models import ExpenseReport
from reports.services.report_generator import ExpenseReportGenerationService

User = get_user_model()


class ExpenseReportGenerationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass123")
        self.user.date_joined = timezone.now() - timedelta(days=30)
        self.user.save()

    @patch("reports.services.report_generator.ExpenseSummaryService")
    @patch("reports.services.report_generator.Expense.objects.filter")
    @patch("reports.services.report_generator.PeriodService.get_next_period_dates")
    def test_generate_reports_creates_reports(
        self, mock_period, mock_expense_filter, mock_summary_service
    ):
        now = timezone.now()

        def fake_period(date_from, period_type):
            return date_from, date_from + timedelta(days=7)

        mock_period.side_effect = fake_period
        mock_expense_filter.return_value = MagicMock()

        summary_instance = MagicMock()
        summary_instance.get_summary.return_value = {"sum": 100}
        summary_instance.get_summary_by_month.return_value = {"months": []}
        mock_summary_service.return_value = summary_instance

        service = ExpenseReportGenerationService(self.user)
        service.now = now

        reports = service.generate_reports()

        self.assertTrue(len(reports) > 0)
        for report in reports:
            self.assertEqual(report.user, self.user)
            self.assertIn(report.report_type, ["weekly", "monthly", "quarter", "year"])

    @patch("reports.services.report_generator.ExpenseSummaryService")
    @patch("reports.services.report_generator.Expense.objects.filter")
    @patch("reports.services.report_generator.PeriodService.get_next_period_dates")
    def test_generate_reports_uses_last_report_date(
        self, mock_period, mock_expense_filter, mock_summary_service
    ):
        last_report = ExpenseReport.objects.create(
            user=self.user,
            date_from=self.user.date_joined,
            date_to=self.user.date_joined + timedelta(days=7),
            report_type="weekly",
            result={"sum": 50},
        )

        def fake_period(date_from, period_type):
            return date_from, date_from + timedelta(days=7)

        mock_period.side_effect = fake_period
        mock_expense_filter.return_value = MagicMock()

        summary_instance = MagicMock()
        summary_instance.get_summary.return_value = {"sum": 200}
        summary_instance.get_summary_by_month.return_value = {"months": []}
        mock_summary_service.return_value = summary_instance

        service = ExpenseReportGenerationService(self.user)
        service.now = timezone.now()

        reports = service.generate_reports()

        weekly_reports = [r for r in reports if r.report_type == "weekly"]
        self.assertTrue(len(weekly_reports) > 0)
        self.assertGreater(weekly_reports[0].date_from, last_report.date_to)
