# Generated by Django 4.2.19 on 2025-04-16 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_blog_blog_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='product.submenu'),
        ),
    ]
