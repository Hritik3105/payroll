# Generated by Django 4.1.3 on 2023-01-09 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0006_providers_manual_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='days_overdue',
            field=models.IntegerField(blank=True, max_length=250, null=True),
        ),
    ]
