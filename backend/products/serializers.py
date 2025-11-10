from rest_framework import serializers
from .models import Product, ProductStatus


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'bot_username', 'website_link',
            'contract_months', 'contract_start_date', 'contract_end_date',
            'is_renewed', 'status', 'customer_telegram', 'customer_link',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_contract_months(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Contract months must be between 1 and 12")
        return value


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'bot_username', 'website_link',
            'contract_months', 'contract_start_date',
            'customer_telegram', 'customer_link'
        ]

    def validate_contract_months(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Contract months must be between 1 and 12")
        return value


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'bot_username', 'website_link',
            'contract_months', 'contract_start_date',
            'customer_telegram', 'customer_link'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'contract_months': {'required': False},
            'contract_start_date': {'required': False},
        }

    def validate_contract_months(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Contract months must be between 1 and 12")
        return value


class DashboardStatsSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    active_products = serializers.IntegerField()
    expired_products = serializers.IntegerField()
    expiring_in_7_days = serializers.IntegerField()
    expiring_in_30_days = serializers.IntegerField()
