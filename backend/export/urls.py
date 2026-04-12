from django.urls import path

from .views import CreateExportResultView, ExportResultDetailView

urlpatterns = [
    path("create/", CreateExportResultView.as_view(), name="create_export"),
    path(
        "result/<uuid:export_result_id>/",
        ExportResultDetailView.as_view(),
        name="export_detail",
    ),
]
