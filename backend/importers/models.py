from django.db import models
from django.conf import settings


class ImportSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="import_sessions")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="imports/")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ], default="pending")
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ImportSession({self.user.username}, {self.uploaded_at}, {self.status})"
class BankProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    delimiter = models.CharField(max_length=5, default=',')
    date_format = models.CharField(max_length=64, default='%Y-%m-%d')
    col_date = models.CharField(max_length=64, default='date')
    col_amount = models.CharField(max_length=64, default='amount')
    col_currency = models.CharField(max_length=64, default='currency')
    col_description = models.CharField(max_length=64, default='description')
    col_category = models.CharField(max_length=64, default='category')
    def __str__(self):
        return self.name

class ImportDedup(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='import_dedup')
    row_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'row_hash')
        indexes = [models.Index(fields=['user','row_hash'])]