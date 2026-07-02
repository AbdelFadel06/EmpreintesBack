from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryDetailView,
    ProductListView, ProductDetailView, ProductByCategoryView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductImageUploadView, ProductImageDeleteView
)

app_name = 'products'

urlpatterns = [
    # Catégories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),  # 👈 NOUVEAU
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    # Produits
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:category_slug>/', ProductByCategoryView.as_view(), name='product-by-category'),

    # Admin CRUD
    path('admin/create/', ProductCreateView.as_view(), name='product-create'),
    path('admin/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('admin/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Images
    path('<int:product_id>/images/upload/', ProductImageUploadView.as_view(), name='image-upload'),
    path('images/<int:id>/delete/', ProductImageDeleteView.as_view(), name='image-delete'),
]
