from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer, ProductListSerializer,
    ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductImageSerializer
)

# ==================== CATÉGORIES ====================
class CategoryListView(generics.ListAPIView):
    """
    Liste de toutes les catégories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryCreateView(generics.CreateAPIView):
    """
    Créer une nouvelle catégorie (admin uniquement)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Détail d'une catégorie avec ses produits
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


# ==================== PRODUITS ====================
class ProductListView(generics.ListAPIView):
    """
    Liste de tous les produits disponibles
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)

        # Filtres optionnels
        category = self.request.query_params.get('category')
        gender = self.request.query_params.get('gender')

        if category:
            queryset = queryset.filter(category__slug=category)
        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset.order_by('-created_at')


class ProductDetailView(generics.RetrieveAPIView):
    """
    Détail complet d'un produit
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class ProductByCategoryView(generics.ListAPIView):
    """
    Liste des produits d'une catégorie spécifique
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        return Product.objects.filter(
            category__slug=category_slug,
            is_available=True
        ).order_by('-created_at')


# ==================== CRUD PRODUITS (ADMIN) ====================
class ProductCreateView(generics.CreateAPIView):
    """
    Créer un nouveau produit
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    """
    Mettre à jour un produit
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


class ProductDeleteView(generics.DestroyAPIView):
    """
    Supprimer un produit
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'


# ==================== GESTION DES IMAGES ====================
class ProductImageUploadView(APIView):
    """
    Ajouter une image à un produit
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if not request.FILES.get('image'):
            return Response(
                {'error': 'Aucune image fournie.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = ProductImage.objects.create(
            product=product,
            image=request.FILES['image'],
            color=request.data.get('color', ''),
            color_code=request.data.get('color_code', ''),
            order=request.data.get('order', 0)
        )

        serializer = ProductImageSerializer(image, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductImageDeleteView(generics.DestroyAPIView):
    """
    Supprimer une image d'un produit
    """
    queryset = ProductImage.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
