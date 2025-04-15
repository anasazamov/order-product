from django.urls import path
from product.views import BlogViewSet, ProductViewSet, ContactViewSet, OrderViewSet, RegionAPIView, MenuViewSet, SubMenuViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'product-type', ProductTypeViewSet, basename='product-type')
router.register(r'product', ProductViewSet, basename='product')
# router.register(r'blog-type', BlogTypeViewSet,  basename='blog-type')
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'submenu', SubMenuViewSet, basename='submenu')

urlpatterns = router.urls
urlpatterns += [
    path('regions-statuses/', RegionAPIView.as_view()),
    
]

