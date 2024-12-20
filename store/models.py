from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  permission = models.CharField(max_length=20, choices=[('Quản lý', 'Quản lý'), ('Nhân viên', 'Nhân viên'), ('Khách hàng', 'Khách hàng')], default='Khách hàng')
  phone_number = models.CharField(max_length=10)
  address = models.CharField(max_length=200)
  city = models.CharField(max_length=50)
  province = models.CharField(max_length=50)
  
  def __str__(self):
    return f'Hồ sơ của {self.user.username}'
  

class Category(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField(max_length=100)
  
  def __str__(self):
    return self.name


class Product(models.Model):
  title = models.CharField(max_length=500)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  slug = models.SlugField(max_length=500, blank=True, null=True)
  thumbnail = models.URLField(max_length=255)
  price_import = models.DecimalField(max_digits=10, decimal_places=0)
  price_export = models.DecimalField(max_digits=10, decimal_places=0)
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    super(Product, self).save(*args, **kwargs)
    
  def __str__(self):
    return self.title
  
  

  