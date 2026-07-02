from django.db import models
from django.conf import settings
from apps.products.models import Product


class Order(models.Model):
  STATUS_CHOICES = [
        ('PENDING', 'En attente de paiement'),
        ('PAID', 'Payée'),
        ('IN_PROGRESS', 'En fabrication'),
        ('SHIPPED', 'Expédiée'),
        ('DELIVERED', 'Livrée'),
        ('CANCELLED', 'Annulée'),
    ]
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
  order_number = models.CharField(max_length=20,unique=True)
  delivery_address = models.TextField()
  phone = models.CharField(max_length=15)
  total_amount = models.DecimalField(max_digits=10, decimal_places=0)
  is_paid = models.BooleanField(default=False)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  estimated_delivery_date = models.DateField(blank=True, null=True)


  def __str__(self):
    return f"{self.order_number} - {self.user.username}"


  def save(self, *args, **kwargs):
    if not self.order_number:
      import datetime
      year = datetime.datetime.now().year
      count = Order.objects.filter(created_at__year = year).count() + 1
      self.order_number = f"EMP-{year}-{str(count).zfill(4)}"
    super().save(*args, **kwargs)




class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=100)
  color = models.CharField(max_length=30)
  size = models.CharField(max_length=10)
  price = models.DecimalField(max_digits=10, decimal_places=0)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f"{self.product_name} - {self.color} - Taille {self.size}"




class Cart(models.Model):
    """Modèle pour stocker le panier en base de données"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    items = models.JSONField(default=dict)  # Stocke le panier en JSON
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def get_total(self):
        """Calculer le total du panier"""
        total = 0
        for item in self.items.values():
            try:
                product = Product.objects.get(id=item['product_id'])
                total += product.base_price * item['quantity']
            except Product.DoesNotExist:
                pass
        return total

    def get_items_count(self):
        """Nombre d'articles dans le panier"""
        return sum(item['quantity'] for item in self.items.values())
