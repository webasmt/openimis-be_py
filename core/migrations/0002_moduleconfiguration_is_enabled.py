# Generated by Django 4.2.16 on 2024-10-25 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduleconfiguration',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]