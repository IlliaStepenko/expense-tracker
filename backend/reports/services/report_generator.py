from datetime import timedelta

from django.utils import timezone
from expenses.models import Expense
from expenses.services import ExpenseSummaryService
from reports.models import ExpenseReport
from reports.services.period_tracker import PeriodService

PERIODS = ["weekly", "monthly", "quarter", "year"]


class ExpenseReportGenerationService:
    def __init__(self, user):
        self.user = user
        self.now = timezone.now()

    def generate_reports(self):
        created_reports = []
        for period_type in PERIODS:
            last_report = (
                ExpenseReport.objects.filter(user=self.user, report_type=period_type)
                .order_by("-date_to")
                .first()
            )

            date_from = (
                last_report.date_to + timedelta(seconds=1)
                if last_report
                else self.user.date_joined
            )

            while date_from < self.now:
                date_from_period, date_to_period = PeriodService.get_next_period_dates(
                    date_from, period_type
                )

                if date_to_period > self.now:
                    date_to_period = self.now

                expenses_qs = Expense.objects.filter(
                    user=self.user,
                    expense_date__gte=date_from_period,
                    expense_date__lte=date_to_period,
                )

                summary_service = ExpenseSummaryService(expenses_qs)
                if period_type in ["weekly", "monthly"]:
                    result = summary_service.get_summary(
                        start_date=date_from_period, end_date=date_to_period
                    )
                else:  # quarter и year
                    result = summary_service.get_summary_by_month(
                        start_date=date_from_period, end_date=date_to_period
                    )

                report = ExpenseReport.objects.create(
                    user=self.user,
                    date_from=date_from_period,
                    date_to=date_to_period,
                    report_type=period_type,
                    result=result,
                    is_viewed=False,
                )
                created_reports.append(report)

                date_from = date_to_period + timedelta(seconds=1)

        return created_reports
