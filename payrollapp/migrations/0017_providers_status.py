# Generated by Django 4.1.3 on 2023-02-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0016_alter_amountpaid_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='providers',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
