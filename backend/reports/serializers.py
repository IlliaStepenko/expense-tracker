from reports.models import ExpenseReport
from rest_framework import serializers


class ExpenseReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseReport
        fields = ["id", "created_at", "report_type", "is_viewed"]


class ExpenseReportMarkViewedSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class ExpenseReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseReport
        fields = [
            "id",
            "date_from",
            "date_to",
            "result",
            "is_viewed",
            "report_type",
            "created_at",
        ]
        read_only_fields = fields
