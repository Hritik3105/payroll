# Generated by Django 4.1.3 on 2023-03-02 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0026_sii_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='providers',
            name='updated_at',
            field=models.DateField(null=True),
        ),
    ]
