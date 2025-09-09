
from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # e.g. USD, EUR
    name = models.CharField(max_length=64)              # e.g. US Dollar
    symbol = models.CharField(max_length=8)             # e.g. $

    def __str__(self):
        return f"{self.code} ({self.symbol})"


class TransactionCategory(models.Model):
    name = models.CharField(max_length=64)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return f"{'Income' if self.is_income else 'Expense'}: {self.name}"

from django.db import models
from django.conf import settings


class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=128)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress(self):
        return min(100, (self.current_amount / self.target_amount) * 100) if self.target_amount else 0

    def __str__(self):
        return f"{self.title} ({self.progress():.0f}%)"


class Reminder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders")
    message = models.CharField(max_length=255)
    remind_at = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} at {self.remind_at}"


class ExchangeRate(models.Model):
    base_code = models.CharField(max_length=3)
    quote_code = models.CharField(max_length=3)
    date = models.DateField()
    rate = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        unique_together = ("base_code", "quote_code", "date")
        indexes = [models.Index(fields=["base_code","quote_code","date"])]


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey('backend.transactions.TransactionCategory', on_delete=models.CASCADE, null=True, blank=True, related_name="budgets")
    month = models.DateField()
    amount_limit = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "category", "month")
        indexes = [models.Index(fields=["user","category","month"])]
