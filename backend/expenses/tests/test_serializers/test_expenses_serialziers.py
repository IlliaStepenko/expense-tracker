from django.contrib.auth import get_user_model
from django.urls import reverse
from expenses.models import Category, Expense
from rest_framework.test import APITestCase

User = get_user_model()


class ExpenseSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.force_authenticate(user=self.user)
        self.default_category = Category.objects.create(user=None, name="Default")

    def test_create_expense_with_existing_category_id(self):
        category = Category.objects.create(user=self.user, name="Food")
        url = reverse("expenses:expenses-list")  # вместо "/expenses/"
        data = {
            "amount": "100.00",
            "category_id": category.id,
            "expense_date": "2026-04-11",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(Expense.objects.first().category, category)

    def test_create_expense_with_new_category_name(self):
        url = reverse("expenses:expenses-list")
        data = {
            "amount": "50.00",
            "category_name": "Health",
            "expense_date": "2026-04-11",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        expense = Expense.objects.first()
        self.assertEqual(expense.category.name, "Health")

    def test_create_expense_with_default_category_name(self):
        url = reverse("expenses:expenses-list")
        data = {
            "amount": "30.00",
            "category_name": "Default",
            "expense_date": "2026-04-11",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        expense = Expense.objects.first()
        self.assertEqual(expense.category, self.default_category)

    def test_error_if_no_category_provided(self):
        url = reverse("expenses:expenses-list")
        data = {"amount": "20.00", "expense_date": "2026-04-11"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "You must specify either category_id or category_name", str(response.data)
        )
