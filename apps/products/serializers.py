from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'color_code', 'image', 'image_url', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer pour la liste des produits (aperçu)
    """
    main_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name',
            'gender', 'base_price', 'is_available', 'main_image'
        ]

    def get_main_image(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer pour le détail d'un produit (complet)
    """
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    available_colors = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'gender',
            'description', 'base_price', 'is_available',
            'production_day', 'created_at', 'updated_at',
            'images', 'available_colors'
        ]

    def get_available_colors(self, obj):
        """
        Récupère les couleurs disponibles pour un produit
        """
        # Utiliser values_list au lieu de distinct pour SQLite
        colors = obj.images.all().values_list('color', flat=True).distinct()
        return list(colors)

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour créer/mettre à jour un produit (admin)
    """
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'gender', 'description',
            'base_price', 'is_available', 'production_day'
        ]
