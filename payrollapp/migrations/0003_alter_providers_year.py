# Generated by Django 4.1.3 on 2022-12-23 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0002_providers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='year',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
