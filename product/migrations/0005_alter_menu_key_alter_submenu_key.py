# Generated by Django 4.2.19 on 2025-04-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_blog_blog_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='key',
            field=models.CharField(editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='submenu',
            name='key',
            field=models.CharField(editable=False, max_length=255),
        ),
    ]
