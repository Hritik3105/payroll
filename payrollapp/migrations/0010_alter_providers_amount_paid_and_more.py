# Generated by Django 4.1.3 on 2023-01-12 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0009_alter_providers_total_amount_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='amount_paid',
            field=models.IntegerField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='providers',
            name='total_amount_paid',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
