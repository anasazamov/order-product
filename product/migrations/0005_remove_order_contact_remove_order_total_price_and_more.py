# Generated by Django 4.2.19 on 2025-03-05 19:38

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_product_price_remove_product_product_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default=998990751735, max_length=255, validators=[product.models.validate_phone]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pn', 'Kutilmoqda'), ('cn', 'Gaplashildi'), ('cd', 'Muvaqqiyatli yakunlandi'), ('cnd', 'Bekor qilindi'), ('rc', 'Qayta Gaplashish')], default='Pending', max_length=255),
        ),
    ]
