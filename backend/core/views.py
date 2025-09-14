from rest_framework import viewsets, permissions
from .models import Currency, TransactionCategory, Budget
from .serializers import CurrencySerializer, TransactionCategorySerializer, BudgetSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionCategoryViewSet(viewsets.ModelViewSet):
    queryset = TransactionCategory.objects.all()
    serializer_class = TransactionCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).order_by("-month")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
