import uuid

from django.db import models


class ExpenseReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("quarter", "Quarterly"),
        ("year", "Yearly"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="expense_reports"
    )
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    result = models.JSONField()
    is_viewed = models.BooleanField(default=False)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_from"]
        verbose_name = "Expense Report"
        verbose_name_plural = "Expense Reports"

    def __str__(self):
        return (
            f"{self.user.username} - {self.report_type} report "
            f"from {self.date_from.date()} to {self.date_to.date()}"
        )
