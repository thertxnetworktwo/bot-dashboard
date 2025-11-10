from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from datetime import datetime, timedelta
from .models import Product, ProductStatus
from .serializers import (
    ProductSerializer, 
    ProductCreateSerializer, 
    ProductUpdateSerializer,
    DashboardStatsSerializer
)


class ProductPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'per_page'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Filter by status
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(bot_username__icontains=search) |
                Q(customer_telegram__icontains=search)
            )
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            # Transform response to match FastAPI format
            return Response({
                'total': response.data['count'],
                'page': int(request.query_params.get('page', 1)),
                'per_page': len(serializer.data),
                'products': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics."""
        now = datetime.utcnow()
        seven_days = now + timedelta(days=7)
        thirty_days = now + timedelta(days=30)

        stats = {
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(status=ProductStatus.ACTIVE).count(),
            'expired_products': Product.objects.filter(status=ProductStatus.EXPIRED).count(),
            'expiring_in_7_days': Product.objects.filter(
                contract_end_date__lte=seven_days,
                contract_end_date__gte=now,
                status__in=[ProductStatus.ACTIVE, ProductStatus.EXPIRING_SOON]
            ).count(),
            'expiring_in_30_days': Product.objects.filter(
                contract_end_date__lte=thirty_days,
                contract_end_date__gte=now,
                status__in=[ProductStatus.ACTIVE, ProductStatus.EXPIRING_SOON]
            ).count(),
        }

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def renew(self, request, pk=None):
        """Renew a product by extending the contract."""
        product = self.get_object()
        months = request.query_params.get('months')
        
        if not months:
            return Response(
                {'detail': 'months parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            months = int(months)
            if months < 1 or months > 12:
                raise ValueError()
        except ValueError:
            return Response(
                {'detail': 'months must be an integer between 1 and 12'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extend contract
        product.contract_end_date = product.contract_end_date + timedelta(days=30 * months)
        product.is_renewed = True
        product.save()
        
        serializer = self.get_serializer(product)
        return Response(serializer.data)
