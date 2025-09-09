from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_code', models.CharField(max_length=3)),
                ('quote_code', models.CharField(max_length=3)),
                ('date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=8, max_digits=18)),
            ],
            options={
                'unique_together': {('base_code', 'quote_code', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('amount_limit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='budgets', to='transactions.transactioncategory')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category', 'month')},
            },
        ),
        migrations.AddIndex(
            model_name='budget',
            index=models.Index(fields=['user', 'category', 'month'], name='core_budge_user_id_5d2c7a_idx'),
        ),
        migrations.AddIndex(
            model_name='exchangerate',
            index=models.Index(fields=['base_code', 'quote_code', 'date'], name='core_excha_base_co_2a47a3_idx'),
        ),
    ]
