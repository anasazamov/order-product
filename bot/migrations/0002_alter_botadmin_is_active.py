# Generated by Django 4.2.19 on 2025-04-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botadmin',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
