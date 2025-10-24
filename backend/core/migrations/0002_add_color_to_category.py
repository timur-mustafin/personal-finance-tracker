from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactioncategory',
            name='color',
            field=models.CharField(default='#9CA3AF', help_text='Hex color like #RRGGBB', max_length=7),
        ),
    ]
