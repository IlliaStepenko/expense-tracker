from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExpenseReportMarkViewedAPIView
from .viewsets import ExpenseReportViewSet

router = DefaultRouter()
router.register(r"", ExpenseReportViewSet, basename="expense_report")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<uuid:report_id>/mark-viewed/",
        ExpenseReportMarkViewedAPIView.as_view(),
        name="expense_report_mark_viewed",
    ),
]
