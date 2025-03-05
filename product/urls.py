from django.urls import path
from product.views import BlogTypeViewSet, BlogViewSet, ProductViewSet, ContactViewSet, OrderViewSet, RegionAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'product-type', ProductTypeViewSet, basename='product-type')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'blog-type', BlogTypeViewSet,  basename='blog-type')
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = router.urls
urlpatterns += [
    path('regions-statuses/', RegionAPIView.as_view()),
    
]

