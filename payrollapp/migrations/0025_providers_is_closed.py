# Generated by Django 4.1.3 on 2023-02-27 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0024_alter_providers_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='providers',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
