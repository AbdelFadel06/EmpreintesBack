from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product
from apps.products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductListSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_detail', 'product_name',
            'color', 'size', 'price', 'quantity', 'subtotal'
        ]
        read_only_fields = ['product_name', 'color', 'size', 'price']

    def get_subtotal(self, obj):
        return obj.price * obj.quantity

class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer pour la liste des commandes (aperçu)
    """
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'total_amount', 'status',
            'is_paid', 'created_at', 'estimated_delivery_date',
            'total_items'
        ]

    def get_total_items(self, obj):
        return obj.items.count()

class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour le détail d'une commande
    """
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'delivery_address',
            'phone', 'total_amount', 'is_paid', 'status',
            'status_display', 'created_at', 'updated_at',
            'estimated_delivery_date', 'items'
        ]
        read_only_fields = ['user', 'order_number']

class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer pour créer une commande depuis le panier
    """
    delivery_address = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    def validate_phone(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Numéro de téléphone invalide.")
        return value

class CartItemSerializer(serializers.Serializer):
    """
    Serializer pour les items du panier (session)
    """
    product_id = serializers.IntegerField()
    color = serializers.CharField()
    size = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
