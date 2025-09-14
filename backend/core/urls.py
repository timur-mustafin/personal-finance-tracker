from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, CurrencyViewSet, TransactionCategoryViewSet

router = DefaultRouter()
router.register(r"currencies", CurrencyViewSet, basename="currencies")
router.register(r"categories", TransactionCategoryViewSet, basename="categories")
router.register(r"budgets", BudgetViewSet, basename="budgets")

urlpatterns = router.urls
