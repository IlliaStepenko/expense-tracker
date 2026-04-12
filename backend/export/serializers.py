from export.models import ExportResult
from rest_framework import serializers


class ExportResultSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = ExportResult
        fields = ["id", "status", "download_url"]
        read_only_fields = ["id", "status", "download_url"]

    def get_download_url(self, obj):
        request = self.context.get("request")
        if obj.status == "SUCCESS" and obj.file_path:
            return request.build_absolute_uri(obj.file_path.url)
        return None


class ExportResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportResult
        fields = [
            "params",
        ]
        extra_kwargs = {"params": {"required": False}}

    def create(self, validated_data):
        user = self.context["request"].user
        export_result = ExportResult.objects.create(
            user=user,
            format="csv",
            params=validated_data.get("params", {}),
            status="PENDING",
        )
        return export_result


class ExportResultSimpleResponseSerializer(serializers.Serializer):
    export_result_id = serializers.UUIDField()
    status = serializers.CharField(max_length=10)
