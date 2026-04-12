from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from expenses.models import Category, Expense
from expenses.services import ExpenseSummaryService

User = get_user_model()


class ExpenseSummaryServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.cat_food = Category.objects.create(user=self.user, name="Food")
        self.cat_health = Category.objects.create(user=self.user, name="Health")
        Expense.objects.create(
            user=self.user,
            category=self.cat_food,
            amount=100,
            expense_date=timezone.now(),
        )
        Expense.objects.create(
            user=self.user,
            category=self.cat_food,
            amount=50,
            expense_date=timezone.now(),
        )
        Expense.objects.create(
            user=self.user,
            category=self.cat_health,
            amount=75,
            expense_date=timezone.now(),
        )

    def test_get_total(self):
        qs = Expense.objects.filter(user=self.user)
        service = ExpenseSummaryService(qs)
        total = service.get_total()
        self.assertEqual(total, Decimal("225.00"))

    def test_get_per_category(self):
        qs = Expense.objects.filter(user=self.user)
        service = ExpenseSummaryService(qs)
        per_category = service.get_per_category()
        expected = [
            {"id": self.cat_food.id, "name": "Food", "total": "150.00"},
            {"id": self.cat_health.id, "name": "Health", "total": "75.00"},
        ]
        per_category_sorted = sorted(per_category, key=lambda x: x["name"])
        expected_sorted = sorted(expected, key=lambda x: x["name"])
        self.assertEqual(per_category_sorted, expected_sorted)

    def test_get_summary_with_dates(self):
        qs = Expense.objects.filter(user=self.user)
        service = ExpenseSummaryService(qs)
        summary = service.get_summary(start_date="2026-04-01", end_date="2026-04-30")
        self.assertEqual(summary["start_date"], "2026-04-01")
        self.assertEqual(summary["end_date"], "2026-04-30")
        self.assertEqual(summary["total"], "225.00")
        self.assertEqual(len(summary["per_category"]), 2)
