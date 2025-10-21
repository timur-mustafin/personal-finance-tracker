from django.db import models
from django.conf import settings
from core.models import Currency, TransactionCategory

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"], name="idx_user_date"),
            models.Index(fields=["user", "category", "date"], name="idx_user_cat_date"),
        ]

    def __str__(self):
        return f"{self.user} {self.amount} {self.currency} on {self.date}"
