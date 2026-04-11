from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryListView, ExpenseViewSet

app_name = "expenses"

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expenses")

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
] + router.urls
