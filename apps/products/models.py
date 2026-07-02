from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)

  def __str__(self):
    return self.name


class Product(models.Model):
  GENDER_CHOICES = [
    ('H','Homme'),
    ('F','Femme'),
    ('U','Unisexe'),
  ]

  name = models.CharField(max_length=100)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
  gender = models.CharField( max_length=1 ,choices=GENDER_CHOICES)
  description = models.TextField()
  base_price = models.DecimalField(max_digits=10, decimal_places=0)
  is_available = models.BooleanField(default=True)
  production_day = models.PositiveIntegerField(default=14)
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.name} -- ({self.get_gender_display()})"



class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
  color = models.CharField(max_length=30)
  color_code = models.CharField(max_length=7, blank=True, null=True)
  image = models.ImageField(upload_to='products/')
  order = models.PositiveIntegerField(default=0)


  class Meta:
    ordering = ['order']
    unique_together = ('product', 'color')


  def __str__(self):
    return f"{self.product.name} -- {self.color}"


