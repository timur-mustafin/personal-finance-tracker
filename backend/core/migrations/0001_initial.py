from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('symbol', models.CharField(blank=True, default='', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_income', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=3)),
                ('target', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=8, max_digits=18)),
            ],
            options={
                'indexes': [models.Index(fields=['base', 'target', 'date'], name='core_exchan_base_ta_3d5f1a_idx')],
                'unique_together': {('base', 'target', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text='Use first day of month')),
                ('limit_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=models.deletion.CASCADE, to='core.transactioncategory')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'category', 'month'], name='core_budget_user_cat_3a5880_idx')],
                'unique_together': {('user', 'category', 'month')},
            },
        ),
    ]
