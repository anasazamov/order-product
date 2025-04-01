from rest_framework import viewsets
from .models import Product, Blog, Contact, Order
from .serializers import ProductSerializer, BlogSerializer, ContactSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.query_params.get('search') is not None:
            return super().get_queryset().filter(name__icontains=self.request.query_params.get('search'))
        return super().get_queryset()
    
    @extend_schema(parameters=[
        OpenApiParameter(name='search', required=False, type=str, location=OpenApiParameter.QUERY, description='Search by name'),]
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# class BlogTypeViewSet(viewsets.ModelViewSet):
#     queryset = BlogType.objects.all()
#     serializer_class = BlogTypeSerializer
#     # permission_classes = [IsAuthenticated]

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def get_queryset(self):
        if self.request.query_params.get('blog_type') is not None and self.request.query_params.get('blog_type') != " ":
            return super().get_queryset().filter(blog_type=self.request.query_params.get('blog_type'))
        if self.request.query_params.get('search') is not None:
            return super().get_queryset().filter(title__icontains=self.request.query_params.get('search'))
        return super().get_queryset()
    
    @extend_schema(parameters=[
        OpenApiParameter(name='blog_type', required=False, type=str, location=OpenApiParameter.QUERY, description='Filter by blog type'),
        OpenApiParameter(name='search', required=False, type=str, location=OpenApiParameter.QUERY, description='Search by title'),]
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update']:
            return [AllowAny()]
        return [IsAuthenticated()]

class RegionAPIView(APIView):
    def get(self, request):
        region = []
        status = []
        regions = Order.UZB_REGIONS
        statuses = Order.STATUS_TYPES
        
        for label, name in regions:
            region.append({
                'label': label,
                'name': name
            })
        
        for label, name in statuses:
            status.append({
                'label': label,
                'name': name
            })
        
        return Response({
            'regions': region,
            'statuses': status
        })
    


