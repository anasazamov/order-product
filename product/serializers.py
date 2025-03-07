from rest_framework import serializers
from .models import Product, Blog, Contact, Order

# class ProductTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductType
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False)
    description = serializers.CharField(required=False)
    class Meta:
        model = Product
        fields = '__all__'

# class BlogTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogType
#         fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):  
    photo = serializers.ImageField(required=False) 
    description = serializers.CharField(required=False)
    class Meta:
        model = Blog
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
# Compare this snippet from product/views.py: