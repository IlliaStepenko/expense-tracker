from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from expenses.models import Category, Expense
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class ExpenseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_expense_with_category_id(self):
        category = Category.objects.create(user=self.user, name="Food")

        url = reverse("expenses:expenses-list")
        data = {
            "amount": "123.45",
            "expense_date": "2026-04-10",
            "description": "Grocery shopping",
            "category_id": category.id,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Expense.objects.filter(user=self.user, category=category).exists()
        )
        self.assertEqual(Decimal(response.data["amount"]), Decimal("123.45"))
        self.assertEqual(response.data["category"]["name"], category.name)

    def test_create_expense_with_category_name(self):
        url = reverse("expenses:expenses-list")
        data = {
            "amount": "50.00",
            "expense_date": "2026-04-10",
            "description": "Lunch",
            "category_name": "Entertainment",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = Category.objects.get(name="Entertainment")
        expense = Expense.objects.get(user=self.user, category=category)

        self.assertEqual(expense.amount, Decimal("50.00"))

    def test_create_expense_negative_amount(self):
        url = reverse("expenses:expenses-list")
        data = {
            "amount": "-10.00",
            "expense_date": "2026-04-10",
            "description": "Invalid expense",
            "category_name": "Food",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Amount must be 0 or greater.", str(response.data))

    def test_report_endpoint(self):
        category = Category.objects.create(user=self.user, name="Food")

        Expense.objects.create(
            user=self.user, category=category, amount=100, expense_date="2026-04-01"
        )
        Expense.objects.create(
            user=self.user, category=category, amount=50, expense_date="2026-04-05"
        )

        url = reverse("expenses:expenses-report")
        response = self.client.get(
            url, {"start_date": "2026-04-01", "end_date": "2026-04-30"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total", response.data)
        self.assertEqual(Decimal(response.data["total"]), Decimal("150.00"))
        self.assertEqual(len(response.data["per_category"]), 1)
        self.assertEqual(response.data["per_category"][0]["total"], "150.00")
        self.assertEqual(response.data["per_category"][0]["name"], category.name)
