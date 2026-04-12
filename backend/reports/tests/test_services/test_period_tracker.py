from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from reports.services.period_tracker import PeriodService


class PeriodServiceTests(TestCase):
    def setUp(self):
        self.base_date = datetime(2024, 1, 1, 0, 0, 0)

    def test_weekly_period(self):
        date_from, date_to = PeriodService.get_next_period_dates(
            self.base_date, "weekly"
        )
        self.assertEqual(date_from, self.base_date)
        self.assertEqual(
            date_to, self.base_date + timedelta(weeks=1) - timedelta(seconds=1)
        )

    def test_monthly_period(self):
        date_from, date_to = PeriodService.get_next_period_dates(
            self.base_date, "monthly"
        )
        self.assertEqual(date_from, self.base_date)
        self.assertEqual(
            date_to, self.base_date + relativedelta(months=1) - timedelta(seconds=1)
        )

    def test_quarter_period(self):
        date_from, date_to = PeriodService.get_next_period_dates(
            self.base_date, "quarter"
        )
        self.assertEqual(date_from, self.base_date)
        self.assertEqual(
            date_to, self.base_date + relativedelta(months=3) - timedelta(seconds=1)
        )

    def test_year_period(self):
        date_from, date_to = PeriodService.get_next_period_dates(self.base_date, "year")
        self.assertEqual(date_from, self.base_date)
        self.assertEqual(
            date_to, self.base_date + relativedelta(years=1) - timedelta(seconds=1)
        )

    def test_invalid_period_type(self):
        with self.assertRaises(ValueError):
            PeriodService.get_next_period_dates(self.base_date, "invalid")
