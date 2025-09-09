from django.urls import path
from .views import summary_by_month, top_categories, budgets_summary

urlpatterns = [
    path("summary/month/", summary_by_month, name="summary-by-month"),
    path("summary/top-categories/", top_categories, name="top-categories"),
    path("budgets/summary/", budgets_summary, name="budgets-summary"),
]
