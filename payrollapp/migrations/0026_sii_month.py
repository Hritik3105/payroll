# Generated by Django 4.1.3 on 2023-03-02 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payrollapp', '0025_providers_is_closed'),
    ]

    operations = [
        migrations.CreateModel(
            name='SII_Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]
