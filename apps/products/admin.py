from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # 3 champs vides par défaut

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'base_price', 'is_available')
    list_filter = ('category', 'gender', 'is_available')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]  # Permet d'ajouter les images directement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
