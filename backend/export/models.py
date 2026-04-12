import uuid

from django.db import models


class ExportResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    FORMAT_CHOICES = [
        ("csv", "CSV"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, blank=True
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default="csv")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    file_path = models.FileField(upload_to="exports/", null=True, blank=True)
    params = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.format} export for {self.user} ({self.status})"
