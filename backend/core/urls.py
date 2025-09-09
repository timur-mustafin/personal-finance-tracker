from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet
try:
    from .views import GoalViewSet, ReminderViewSet, CurrencyViewSet, TransactionCategoryViewSet
except Exception:
    GoalViewSet = GoalViewSet if 'GoalViewSet' in globals() else None
    ReminderViewSet = ReminderViewSet if 'ReminderViewSet' in globals() else None
    CurrencyViewSet = CurrencyViewSet if 'CurrencyViewSet' in globals() else None
    TransactionCategoryViewSet = TransactionCategoryViewSet if 'TransactionCategoryViewSet' in globals() else None

router = DefaultRouter()
if CurrencyViewSet: router.register(r"currencies", CurrencyViewSet)
if TransactionCategoryViewSet: router.register(r"categories", TransactionCategoryViewSet)
if GoalViewSet: router.register(r"goals", GoalViewSet)
if ReminderViewSet: router.register(r"reminders", ReminderViewSet)
router.register(r"budgets", BudgetViewSet, basename="budgets")

urlpatterns = router.urls
