from datetime import timedelta

from dateutil.relativedelta import relativedelta


class PeriodService:
    PERIODS = ["weekly", "monthly", "quarter", "year"]

    @staticmethod
    def get_next_period_dates(last_report_date, period_type):
        if period_type not in PeriodService.PERIODS:
            raise ValueError(f"Unknown period type: {period_type}")
        date_from, date_to = None, None

        if period_type == "weekly":
            date_from = last_report_date
            date_to = date_from + timedelta(weeks=1) - timedelta(seconds=1)
        elif period_type == "monthly":
            date_from = last_report_date
            date_to = date_from + relativedelta(months=1) - timedelta(seconds=1)
        elif period_type == "quarter":
            date_from = last_report_date
            date_to = date_from + relativedelta(months=3) - timedelta(seconds=1)
        elif period_type == "year":
            date_from = last_report_date
            date_to = date_from + relativedelta(years=1) - timedelta(seconds=1)

        return date_from, date_to
