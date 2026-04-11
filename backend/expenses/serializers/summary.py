from decimal import ROUND_HALF_UP, Decimal

from rest_framework import serializers


class CategorySummarySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total = (
            obj["total"] if isinstance(obj["total"], Decimal) else Decimal(obj["total"])
        )
        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{total:.2f}"


class ExpenseSummarySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    total = serializers.SerializerMethodField()
    per_category = CategorySummarySerializer(many=True)

    def get_total(self, obj):
        total = (
            obj["total"] if isinstance(obj["total"], Decimal) else Decimal(obj["total"])
        )
        total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{total:.2f}"
