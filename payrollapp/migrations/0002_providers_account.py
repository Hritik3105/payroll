# Generated by Django 4.1.3 on 2023-01-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='providers',
            name='account',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]