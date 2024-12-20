from django.db import models
from store.models import Product
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Stock(models.Model):
  product = models.OneToOneField(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField(blank=True, null=True)
  purchased = models.IntegerField(default=0)
  inventory = models.IntegerField(blank=True, null=True)
  out_of_stock = models.BooleanField(default=False)
  
  def save(self, *args, **kwargs):
    if self.quantity:
      self.inventory = self.quantity - self.purchased
    if self.inventory and self.inventory < 3:
      self.out_of_stock = True
    else:
      self.out_of_stock = False
    super(Stock, self).save(*args, **kwargs)
  
  def __str__(self):
    return f'Tồn kho {self.product}'

def create_stock(sender, instance, created, **kwargs):
    if created:
        stock = Stock(product=instance)
        stock.save()
post_save.connect(create_stock, sender=Product)
  
  
class Provider(models.Model):
  name = models.CharField(max_length=200)
  address = models.CharField(max_length=500)
  
  def __str__(self):
    return self.name
    

class Import(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
  note = models.TextField()
  created_date = models.DateTimeField(auto_now_add=True)
    
  def __str__(self):
    return f'{self.created_date} nhập kho từ {self.provider.name}'
  
  
class ImportDetail(models.Model):
  _import = models.ForeignKey(Import, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  
  @property
  def total_price(self):
      return self.product.price_import * self.quantity
    
  def __str__(self):
    return f'Chi tiết nhập kho {self._import}'
  

class Export(models.Model):
  created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True, related_name='created_by')
  customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_by')
  store_note = models.TextField(blank=True, null=True)
  customer_note = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=20, choices=[('Chờ duyệt', 'Chờ duyệt'),('Đã xuất', 'Đã xuất'), ('Không xuất', 'Không xuất')], default='Chờ duyệt')
  required_date = models.DateTimeField(auto_now_add=True)
  exported_date = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return f'{self.status} yêu cầu {self.customer.username}'
  

class ExportDetail(models.Model):
  export = models.ForeignKey(Export, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.IntegerField()

  @property
  def total_price(self):
      return self.product.price_export * self.quantity
  
  def __str__(self):
    return f'Chi tiết {self.export}'
  