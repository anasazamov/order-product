# Generated by Django 4.2.19 on 2025-03-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_order_client_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.CharField(default='Blog', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='region',
            field=models.CharField(choices=[('AN', 'Андижан'), ('BU', 'Бухара'), ('FA', 'Фергана'), ('JI', 'Джизак'), ('XO', 'Хорезм'), ('NA', 'Наманган'), ('NG', 'Навои'), ('QA', 'Кашкадарья'), ('QR', 'Каракалпакстан'), ('SA', 'Самарканд'), ('SI', 'Сырдарья'), ('SU', 'Сурхандарья'), ('TO', 'Ташкентская область'), ('TT', 'Город Ташкент')], max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pn', 'В ожидании'), ('cn', 'Обсуждено'), ('cd', 'Успешно завершено'), ('cnd', 'Отменено'), ('rc', 'Повторное обсуждение')], default='Pending', max_length=255),
        ),
        migrations.DeleteModel(
            name='BlogType',
        ),
    ]
