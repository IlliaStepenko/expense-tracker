from celery import shared_task
from reports.services.report_generator import ExpenseReportGenerationService
from users.models import User


@shared_task(bind=True, ignore_result=True)
def generate_expense_reports_task():
    for user in User.objects.all():
        ExpenseReportGenerationService(user).generate_reports()
