from django.db import models
import re
from django.core.exceptions import ValidationError

def validate_phone(value):
    if not re.match(r'^\+?1?\d{9,15}$', value):
        raise ValidationError('Invalid phone number. Enter a valid phone number. Example: +998990751735')

# Create your models here.

class BlogType(models.Model):
    name = models.CharField(max_length=255, null=False)

class Blog(models.Model):
    title = models.CharField(max_length=255, null=False)
    blog_type = models.ForeignKey(BlogType, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank='')
    photo = models.ImageField(upload_to='blog/', null=True)

class ProductType(models.Model):
    name = models.CharField(max_length=255, null=False)

class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(blank='')
    photo = models.ImageField(upload_to='product/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)



class Contact(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False, validators=[validate_phone])
    message = models.TextField(blank='')

class Order(models.Model):
    
    UZB_REGIONS = [
            ('AN', 'Andijon'),
            ('BU', 'Buxoro'),
            ('FA', 'Farg‘ona'),
            ('JI', 'Jizzax'),
            ('XO', 'Xorazm'),
            ('NA', 'Namangan'),
            ('NG', 'Navoiy'),
            ('QA', 'Qashqadaryo'),
            ('QR', 'Qoraqalpog‘iston'),
            ('SA', 'Samarqand'),
            ('SI', 'Sirdaryo'),
            ('SU', 'Surxondaryo'),
            ('TO', 'Toshkent viloyati'),
            ('TT', 'Toshkent shahri'),
        ]
    
    STATUS_TYPES = [
            ('Pending', 'Pending'),
            ('Conversion', 'Conversion'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
            ('Refunded', 'Refunded'),
        ]
    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=255, null=False, default='Pending', choices=STATUS_TYPES)
    region = models.CharField(max_length=255, null=False, choices=UZB_REGIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



