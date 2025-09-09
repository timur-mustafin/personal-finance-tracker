from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
		('importers', '0001_initial'),
	]
	operations = [
		migrations.CreateModel(
			name='BankProfile',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('name', models.CharField(max_length=100, unique=True)),
				('delimiter', models.CharField(default=',', max_length=5)),
				('date_format', models.CharField(default='%Y-%m-%d', max_length=64)),
				('col_date', models.CharField(default='date', max_length=64)),
				('col_amount', models.CharField(default='amount', max_length=64)),
				('col_currency', models.CharField(default='currency', max_length=64)),
				('col_description', models.CharField(default='description', max_length=64)),
				('col_category', models.CharField(default='category', max_length=64)),
			]
		),
		migrations.CreateModel(
			name='ImportDedup',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('row_hash', models.CharField(max_length=64)),
				('created_at', models.DateTimeField(auto_now_add=True)),
				('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='import_dedup', to=settings.AUTH_USER_MODEL)),
			],
			options={
				'unique_together': {('user', 'row_hash')},
			},
		),
		migrations.AddIndex(
			model_name='importdedup',
			index=models.Index(fields=['user', 'row_hash'], name='importers_i_user_id__3f1159_idx')
		),
	]