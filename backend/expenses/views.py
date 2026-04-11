from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import ExpenseFilter
from .models import Category, Expense
from .serializers import (
    CategoryListSerializer,
    ExpenseSerializer,
    ExpenseSummarySerializer,
)
from .services import ExpenseSummaryService


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(Q(is_default=True) | Q(user=user))
        return queryset.distinct()


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def report(self, request):
        qs = self.filter_queryset(self.get_queryset())

        summary_service = ExpenseSummaryService(qs)
        summary_data = summary_service.get_summary(
            start_date=request.query_params.get("start_date"),
            end_date=request.query_params.get("end_date"),
        )

        serializer = ExpenseSummarySerializer(summary_data)

        return Response(serializer.data)
