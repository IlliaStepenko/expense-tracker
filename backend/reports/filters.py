from datetime import datetime, time

from django.utils.timezone import make_aware
from django_filters import rest_framework as filters
from reports.models import ExpenseReport


class ExpenseReportFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="created_at", method="filter_end_date")

    class Meta:
        model = ExpenseReport
        fields = ["report_type", "is_viewed", "report_type"]

    def filter_end_date(self, queryset, name, value):
        end_of_day = make_aware(datetime.combine(value, time.max))
        return queryset.filter(created_at__lte=end_of_day)
