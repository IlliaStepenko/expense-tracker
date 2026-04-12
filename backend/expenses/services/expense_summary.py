from calendar import monthrange
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Sum


class ExpenseSummaryService:
    def __init__(self, queryset):
        self.queryset = queryset

    def get_total(self):
        total = self.queryset.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_per_category(self):
        per_category_qs = self.queryset.values(
            "category__id", "category__name"
        ).annotate(category_total=Sum("amount"))
        return [
            {
                "id": item["category__id"],
                "name": item["category__name"],
                "total": str(
                    Decimal(item["category_total"] or 0).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                ),
            }
            for item in per_category_qs
        ]

    def get_summary(self, start_date=None, end_date=None):
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total": str(self.get_total()),
            "per_category": self.get_per_category(),
        }

    def get_summary_by_month(self, start_date=None, end_date=None):
        report = {}
        current = datetime(start_date.year, start_date.month, 1)
        last = datetime(end_date.year, end_date.month, 1)

        while current <= last:
            month_start = current
            month_end = datetime(
                current.year,
                current.month,
                monthrange(current.year, current.month)[1],
                23,
                59,
                59,
            )

            month_qs = self.queryset.filter(
                expense_date__gte=month_start, expense_date__lte=month_end
            )

            month_summary = {}
            for item in month_qs.values("category__name").annotate(total=Sum("amount")):
                month_summary[item["category__name"]] = str(
                    Decimal(item["total"] or 0).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                )

            report[current.strftime("%Y-%m")] = month_summary

            if current.month == 12:
                current = datetime(current.year + 1, 1, 1)
            else:
                current = datetime(current.year, current.month + 1, 1)

        return report
