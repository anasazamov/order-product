from django.db import models
import re
from django.core.exceptions import ValidationError

def validate_phone(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('Invalid phone number. Enter a valid phone number. Example: +998990751735')

# Create your models here.

# class BlogType(models.Model):
#     name = models.CharField(max_length=255, null=False)

class Blog(models.Model):
    title = models.CharField(max_length=255, null=False)
    blog_type = models.CharField(max_length=255, null=False)
    description = models.TextField(blank='')
    photo = models.ImageField(upload_to='blog/', null=True)

class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank='')
    photo = models.ImageField(upload_to='product/', null=True)

class Contact(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False, validators=[validate_phone])
    message = models.TextField(blank='')

class Order(models.Model):
    
    UZB_REGIONS = [
        ('AN', 'Андижан'),
        ('BU', 'Бухара'),
        ('FA', 'Фергана'),
        ('JI', 'Джизак'),
        ('XO', 'Хорезм'),
        ('NA', 'Наманган'),
        ('NG', 'Навои'),
        ('QA', 'Кашкадарья'),
        ('QR', 'Каракалпакстан'),
        ('SA', 'Самарканд'),
        ('SI', 'Сырдарья'),
        ('SU', 'Сурхандарья'),
        ('TO', 'Ташкентская область'),
        ('TT', 'Город Ташкент'),
    ]

    STATUS_TYPES = [
        ('pn', 'В ожидании'),
        ('cn', 'Обсуждено'),
        ('cd', 'Успешно завершено'),
        ('cnd', 'Отменено'),
        ('rc', 'Повторное обсуждение'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    client_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=255, null=False, validators=[validate_phone])
    status = models.CharField(max_length=255, null=False, default='Pending', choices=STATUS_TYPES)
    region = models.CharField(max_length=255, null=False, choices=UZB_REGIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



