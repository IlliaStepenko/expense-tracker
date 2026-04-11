from datetime import datetime, time

from django.utils.timezone import make_aware
from django_filters import rest_framework as filters

from .models import Expense


class ExpenseFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="expense_date", method="filter_end_date")
    category = filters.NumberFilter(field_name="category__id")

    class Meta:
        model = Expense
        fields = ["start_date", "end_date", "category"]

    def filter_end_date(self, queryset, name, value):
        end_of_day = make_aware(datetime.combine(value, time.max))
        return queryset.filter(expense_date__lte=end_of_day)
