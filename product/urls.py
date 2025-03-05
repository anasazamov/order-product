from django.urls import path
from product.views import BlogTypeViewSet, BlogViewSet, ProductTypeViewSet, ProductViewSet, ContactViewSet, OrderViewSet, RegionAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product-type', ProductTypeViewSet)
router.register('product', ProductViewSet)
router.register('blog-type', BlogTypeViewSet)
router.register('blog', BlogViewSet)
router.register('contact', ContactViewSet)
router.register('order', OrderViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('region/', RegionAPIView.as_view())
]

