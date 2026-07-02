from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  phone = models.CharField(max_length=15, unique = True)
  address = models.TextField(null=True, blank=True)
  email = models.EmailField(unique=True)


  def __str__(self):
    return f"{self.username} - {self.phone}"
