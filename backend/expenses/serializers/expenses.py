from rest_framework import serializers

from ..models import Category, Expense
from .categories import CategoryNestedSerializer


class ExpenseSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True, required=False)
    category_name = serializers.CharField(write_only=True, required=False)
    category = CategoryNestedSerializer(read_only=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "expense_date",
            "description",
            "category_id",
            "category_name",
            "category",
        ]
        read_only_fields = ["id", "category"]

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be 0 or greater.")
        return value

    def validate(self, attrs):
        category_id = attrs.pop("category_id", None)
        category_name = attrs.pop("category_name", None)
        user = self.context["request"].user

        if not category_id and not category_name:
            raise serializers.ValidationError(
                "You must specify either category_id or category_name."
            )

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    f"Category with id={category_id} not found"
                )
        else:
            category = Category.objects.filter(user=user, name=category_name).first()
            if not category:
                category = Category.objects.filter(
                    user__isnull=True, name=category_name
                ).first()
            if not category:
                category = Category.objects.create(user=user, name=category_name)

        attrs["category"] = category
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
