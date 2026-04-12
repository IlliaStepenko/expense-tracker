import csv
import os

from celery import shared_task
from django.conf import settings
from expenses.models import Expense
from export.models import ExportResult


@shared_task(bind=True)
def generate_export(self, export_result_id):
    export_result = ExportResult.objects.get(id=export_result_id)
    try:
        export_result.status = "PENDING"
        export_result.save()

        params = export_result.params or {}
        queryset = Expense.objects.all()

        queryset = queryset.filter(user_id=export_result.user.id)

        if "category_id" in params:
            queryset = queryset.filter(category_id=params["category_id"])
        if "start_date" in params:
            queryset = queryset.filter(expense_date__gte=params["start_date"])
        if "end_date" in params:
            queryset = queryset.filter(expense_date__lte=params["end_date"])

        file_name = f"{export_result.id}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, "export", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["User", "Date", "Category", "Amount", "Description"])
            for expense in queryset:
                writer.writerow(
                    [
                        expense.user.username,
                        expense.expense_date,
                        expense.category.name,
                        expense.quantized_amount,
                        expense.description,
                    ]
                )

        export_result.file_path = f"export/{file_name}"
        export_result.status = "SUCCESS"
        export_result.save()

    except Exception as e:
        export_result.status = "FAILED"
        export_result.error_message = str(e)
        export_result.save()
        raise self.retry(exc=e, countdown=60, max_retries=3)
