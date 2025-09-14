from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='core.transactioncategory')),
                ('currency', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='core.currency')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
    ]
