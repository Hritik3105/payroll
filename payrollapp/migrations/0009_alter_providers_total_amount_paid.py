# Generated by Django 4.1.3 on 2023-01-12 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0008_providers_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='total_amount_paid',
            field=models.IntegerField(blank=True, max_length=250, null=True),
        ),
    ]
