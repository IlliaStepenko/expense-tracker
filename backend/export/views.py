from django.shortcuts import get_object_or_404
from export.models import ExportResult
from export.serializers import (
    ExportResultCreateSerializer,
    ExportResultSerializer,
    ExportResultSimpleResponseSerializer,
)
from export.tasks.regular import generate_export
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateExportResultView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ExportResultCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        export_result = serializer.save()

        generate_export.delay(str(export_result.id))

        response_serializer = ExportResultSimpleResponseSerializer(
            {"export_result_id": export_result.id, "status": export_result.status}
        )

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ExportResultDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, export_result_id):
        export_result = get_object_or_404(
            ExportResult, id=export_result_id, user=request.user
        )
        serializer = ExportResultSerializer(export_result, context={"request": request})
        return Response(serializer.data)
