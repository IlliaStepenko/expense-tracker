from reports.models import ExpenseReport
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExpenseReportMarkViewedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, report_id):
        try:
            report = ExpenseReport.objects.get(id=report_id, user=request.user)
        except ExpenseReport.DoesNotExist:
            return Response(
                {"detail": "Report not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if not report.is_viewed:
            report.is_viewed = True
            report.save()

        return Response(
            {"id": str(report.id), "is_viewed": report.is_viewed},
            status=status.HTTP_200_OK,
        )
