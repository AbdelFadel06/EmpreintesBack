# apps/orders/views.py
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, Cart
from .serializers import (
    OrderListSerializer, OrderDetailSerializer,
    OrderCreateSerializer, CartItemSerializer
)
from apps.products.models import Product

# ==================== PANIER (BASE DE DONNÉES) ====================
class CartView(APIView):
    """
    Gestion du panier avec stockage en base de données
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_cart(self, user):
        """Récupérer ou créer le panier de l'utilisateur"""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        """Récupérer le contenu du panier"""
        cart = self.get_cart(request.user)
        cart_data = cart.items

        cart_items = []
        total = 0

        for key, item in cart_data.items():
            try:
                product = Product.objects.get(id=item['product_id'], is_available=True)
                subtotal = product.base_price * item['quantity']
                total += subtotal

                cart_items.append({
                    'key': key,
                    'product_id': product.id,
                    'product_name': product.name,
                    'color': item['color'],
                    'size': item['size'],
                    'quantity': item['quantity'],
                    'price': float(product.base_price),
                    'subtotal': float(subtotal),
                    'image': product.images.first().image.url if product.images.first() else None
                })
            except Product.DoesNotExist:
                # Supprimer les produits qui n'existent plus
                del cart_data[key]
                cart.items = cart_data
                cart.save()

        return Response({
            'items': cart_items,
            'total': float(total),
            'total_items': len(cart_items)
        })

    def post(self, request):
        """Ajouter un produit au panier"""
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        color = serializer.validated_data['color']
        size = serializer.validated_data['size']
        quantity = serializer.validated_data['quantity']

        # Vérifier que le produit existe
        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Produit non trouvé'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier la couleur (si des images existent)
        if product.images.exists() and not product.images.filter(color=color).exists():
            available_colors = list(product.images.values_list('color', flat=True).distinct())
            return Response(
                {'error': f'La couleur "{color}" n\'est pas disponible. Disponible: {", ".join(available_colors)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer le panier
        cart = self.get_cart(request.user)
        cart_data = cart.items

        # Clé unique pour ce produit + couleur + pointure
        item_key = f"{product_id}-{color}-{size}"

        if item_key in cart_data:
            cart_data[item_key]['quantity'] += quantity
        else:
            cart_data[item_key] = {
                'product_id': product_id,
                'color': color,
                'size': size,
                'quantity': quantity
            }

        # Sauvegarder
        cart.items = cart_data
        cart.save()

        return Response({
            'message': 'Produit ajouté au panier.',
            'cart_size': len(cart_data)
        }, status=status.HTTP_200_OK)

    def delete(self, request, item_key):
        """Supprimer un item du panier"""
        cart = self.get_cart(request.user)
        cart_data = cart.items

        if item_key in cart_data:
            del cart_data[item_key]
            cart.items = cart_data
            cart.save()
            return Response({'message': 'Item retiré du panier.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Item non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

class CartClearView(APIView):
    """
    Vider complètement le panier
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items = {}
        cart.save()
        return Response({'message': 'Panier vidé.'}, status=status.HTTP_200_OK)

# ==================== COMMANDES ====================
class CheckoutView(APIView):
    """
    Valider la commande (transformer le panier en commande)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Récupérer le panier
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_data = cart.items

        if not cart_data:
            return Response(
                {'error': 'Votre panier est vide.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Valider les données de livraison
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Calculer le total et préparer les items
        total_amount = 0
        order_items = []

        for key, item in cart_data.items():
            try:
                product = Product.objects.get(id=item['product_id'], is_available=True)
                subtotal = product.base_price * item['quantity']
                total_amount += subtotal

                order_items.append({
                    'product': product,
                    'product_name': product.name,
                    'color': item['color'],
                    'size': item['size'],
                    'price': product.base_price,
                    'quantity': item['quantity']
                })
            except Product.DoesNotExist:
                return Response(
                    {'error': f'Le produit {item["product_id"]} n\'est plus disponible.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            delivery_address=serializer.validated_data['delivery_address'],
            phone=serializer.validated_data['phone'],
            total_amount=total_amount,
            is_paid=False,
            status='PENDING',
            estimated_delivery_date=timezone.now().date() + timedelta(days=14)
        )

        # Créer les OrderItems
        for item_data in order_items:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product_name'],
                color=item_data['color'],
                size=item_data['size'],
                price=item_data['price'],
                quantity=item_data['quantity']
            )

        # Vider le panier
        cart.items = {}
        cart.save()

        # Retourner la commande créée
        order_serializer = OrderDetailSerializer(order)
        return Response({
            'message': 'Commande créée avec succès !',
            'order': order_serializer.data,
            'payment_instructions': {
                'bank': 'Virement bancaire à effectuer sur le compte : ...',
                'momo': 'Orange Money / MTN MoMo : ...'
            }
        }, status=status.HTTP_201_CREATED)




class OrderListView(generics.ListAPIView):
    """
    Liste des commandes de l'utilisateur connecté
    """
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    """
    Détail d'une commande spécifique
    """
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCancelView(APIView):
    """
    Annuler une commande (seulement si elle est en attente)
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.status != 'PENDING':
            return Response(
                {'error': 'Cette commande ne peut pas être annulée.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELLED'
        order.save()

        return Response({
            'message': 'Commande annulée avec succès.',
            'order': OrderDetailSerializer(order).data
        }, status=status.HTTP_200_OK)

class OrderStatusView(APIView):
    """
    Vérifier le statut d'une commande (pour le suivi)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        return Response({
            'order_number': order.order_number,
            'status': order.status,
            'status_display': order.get_status_display(),
            'estimated_delivery_date': order.estimated_delivery_date,
            'created_at': order.created_at,
            'is_paid': order.is_paid
        }, status=status.HTTP_200_OK)
