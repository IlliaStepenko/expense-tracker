from django_filters.rest_framework import DjangoFilterBackend
from reports.filters import ExpenseReportFilter
from reports.models import ExpenseReport
from reports.serializers import (
    ExpenseReportDetailSerializer,
    ExpenseReportListSerializer,
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ExpenseReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExpenseReportListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseReportFilter

    def get_queryset(self):
        return ExpenseReport.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ExpenseReportListSerializer
        return ExpenseReportDetailSerializer
