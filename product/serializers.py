from rest_framework import serializers
from .models import Product, Blog, Contact, Order, Menu, SubMenu

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

class CreateMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'label']

class MenuSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField(method_name='get_submenus')
    key = serializers.SerializerMethodField(method_name='get_key')
    label = serializers.CharField(required=True)
    class Meta:
        model = Menu
        fields = ['id', 'label', 'key', 'children']
    
    def get_submenus(self, obj):
        submenus = SubMenu.objects.filter(parent=obj)
        return SubMenuDetailSerializer(submenus, many=True).data
    
    def get_key(self, obj):
        return obj.key



class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = ['label', 'parent']

class SubMenuDetailSerializer(SubMenuSerializer):
    parent = CreateMenuSerializer()

    class Meta:
        model = SubMenu
        fields = ['id', 'label', 'parent', 'key']