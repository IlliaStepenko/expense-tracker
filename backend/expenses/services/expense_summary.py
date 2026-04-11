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
