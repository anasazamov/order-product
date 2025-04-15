from rest_framework import serializers
from .models import Product, Blog, Contact, Order, Menu, SubMenu, OrderItem

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

class OrderItemSerializer(serializers.ModelSerializer):
    # Yozish (write) uchun: mahsulotni faqat uning ID si orqali tanlash.
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product'
    )
    
    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    # Order modelidagi mahsulotlar va ularning miqdorlarini order_items orqali ko'rsatyapmiz.
    order_items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = (
            'id',
            'client_name',
            'phone_number',
            'status',
            'region',
            'created_at',
            'updated_at',
            'order_items'
        )
    
    def create(self, validated_data):
        # order_items ma'lumotlarini ajratib olamiz.
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        # Order yangilanishi jarayonida order_items qismidagi ma'lumotlar bilan ishlash.
        order_items_data = validated_data.pop('order_items', None)
        
        # Asosiy order maydonlarini yangilash
        instance.client_name = validated_data.get('client_name', instance.client_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.status = validated_data.get('status', instance.status)
        instance.region = validated_data.get('region', instance.region)
        instance.save()
        
        if order_items_data is not None:
            # Avval mavjud order_items obyektlarini o'chirib tashlaymiz
            instance.order_items.all().delete()
            # Keyin yangi order_items obyektlarini yaratamiz
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)
        return instance