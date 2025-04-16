from django.contrib import admin
from product.models import Menu, SubMenu, Blog, Product, Contact, Order
# Register your models here.

from django import forms
from product.models import Blog, SubMenu

class BlogForm(forms.ModelForm):
    blog_type = forms.ChoiceField()  

    class Meta:
        model = Blog
        fields = '__all__' 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blog_type'].choices = [
            (submenu.key, submenu.label) for submenu in SubMenu.objects.all()
        ]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['label', 'key']
    search_fields = ['label']
    list_filter = ['label']
    ordering = ['label']
    # list_editable = ['key']

@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ['label', 'parent', 'key']
    search_fields = ['label']
    list_filter = ['parent']
    ordering = ['label']
    # list_editable = ['key']
    # list_select_related = ['parent']
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('parent')
    # def parent(self, obj):
    #     return obj.parent.name
    # parent.short_description = 'Menu'
    # parent.admin_order_field = 'parent__name'
    # parent.boolean = False
    # parent.allow_tags = True
    # parent.empty_value_display = '-empty-'
    # parent.admin_order_field = 'parent__name'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'blog_type']
    search_fields = ['title']
    list_filter = ['blog_type']
    ordering = ['title']
    form = BlogForm
    # list_editable = ['blog_type']
    # list_select_related = ['blog_type']
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('blog_type')
    # def blog_type(self, obj):
    #     return obj.blog_type.name
    # blog_type.short_description = 'Blog Type'
    # blog_type.admin_order_field = 'blog_type__name'
    # blog_type.boolean = False
    # blog_type.allow_tags = True
    # blog_type.empty_value_display = '-empty-'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    # list_editable = ['name']
    # list_select_related = ['name']

    list_per_page = 10
    list_max_show_all = 100
    # list_select_related = ['name']
    # list_prefetch_related = ['name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    search_fields = ['name', 'phone']
    ordering = ['name']
    # list_editable = ['phone']
    # list_select_related = ['name', 'phone']
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('name', 'phone')
    # def name(self, obj):
    #     return obj.name
    # name.short_description = 'Contact Name'
    # name.admin_order_field = 'name'
    # name.boolean = False
    # name.allow_tags = True
    # name.empty_value_display = '-empty-'
    list_per_page = 10
    list_max_show_all = 100

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'region', 'status']
    search_fields = ['region', 'status']
    ordering = ['region']
    # list_editable = ['status']
    # list_select_related = ['region', 'status']
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.select_related('region', 'status')
    # def region(self, obj):
    #     return obj.region
    # region.short_description = 'Order Region'
    # region.admin_order_field = 'region'
    # region.boolean = False
    # region.allow_tags = True
    # region.empty_value_display = '-empty-'
    list_per_page = 10
    list_max_show_all = 100

admin.site.site_header = "Admin Panel"
