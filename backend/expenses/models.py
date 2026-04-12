from decimal import ROUND_HALF_UP, Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False)
    is_default = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Expense(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="expenses"
    )
    expense_date = models.DateTimeField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="expenses"
    )

    def __str__(self):
        return f"{self.amount} - {self.category.name}"

    @property
    def quantized_amount(self):
        return self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
