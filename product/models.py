from django.db import models
import re
from django.core.exceptions import ValidationError
from uuid import uuid4
from product.manager.manager import MenuManager
from ckeditor.fields import RichTextField

def validate_phone(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('Invalid phone number. Enter a valid phone number. Example: +998990751735')

# Create your models here.

class Menu(models.Model):
    label = models.CharField(max_length=255, null=False, unique=True)
    key = models.CharField(max_length=255, null=False, editable=False)

    objects = MenuManager()

    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.label.lower().replace(' ', '_') + str(uuid4())[:2]
        super().save(*args, **kwargs)


class SubMenu(models.Model):
    label = models.CharField(max_length=255, null=False)
    parent = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='submenus')
    key = models.CharField(max_length=255, null=False, editable=False)
    objects = MenuManager()

    def __str__(self):
        return self.label
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.label.lower().replace(' ', '_') + str(uuid4())[:2]
        super().save(*args, **kwargs)
    
def get_submenu_choices():

    return [(submenu.key, submenu.label) for submenu in SubMenu.objects.all()]

class Blog(models.Model):
    title = models.CharField(max_length=255, null=False)
    blog_type = models.CharField(
        max_length=255,
        null=False,
        choices=get_submenu_choices()
    )
    description = RichTextField(blank="")
    photo = models.ImageField(upload_to='blog/', null=True)


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank='')
    photo = models.ImageField(upload_to='product/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False, validators=[validate_phone])
    message = models.TextField(blank='')

    def __str__(self):
        return self.name

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
    
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')
    client_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=255, null=False, validators=[validate_phone])
    status = models.CharField(max_length=255, null=False, default='Pending', choices=STATUS_TYPES)
    region = models.CharField(max_length=255, null=False, choices=UZB_REGIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.client_name} - {self.status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order #{self.order.id}"