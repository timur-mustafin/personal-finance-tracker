from django.db import models
from django.conf import settings

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)
    symbol = models.CharField(max_length=8, blank=True, default="")

    def __str__(self):
        return f"{self.code}"

class TransactionCategory(models.Model):
    name = models.CharField(max_length=64)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'income' if self.is_income else 'expense'})"

class ExchangeRate(models.Model):
    base = models.CharField(max_length=3)
    target = models.CharField(max_length=3)
    date = models.DateField()
    rate = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        unique_together = ("base", "target", "date")
        indexes = [models.Index(fields=["base","target","date"])]

    def __str__(self):
        return f"{self.base}->{self.target} {self.date}: {self.rate}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    month = models.DateField(help_text="Use first day of month")
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user","category","month")
        indexes = [models.Index(fields=["user","category","month"])]

    def __str__(self):
        return f"{self.user} {self.category} @ {self.month}: {self.limit_amount}"
