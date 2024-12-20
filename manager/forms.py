from django import forms
from store.models import Product
from warehouse.models import Provider


class FormProvider(forms.ModelForm):
  class Meta:
    model=Provider
    fields = '__all__'
    labels = {'name': 'Tên nhà cung cấp', 'address': 'Địa chỉ'}
    widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
               'address': forms.TextInput(attrs={'class': 'form-control'})}

class FormProduct(forms.ModelForm):
  class Meta:
    model = Product
    exclude = ('slug', 'created_at')
    labels = {'title': 'Tên sản phẩm', 'category': 'Dòng sản phẩm', 'thumbnail': 'Link ảnh sản phẩm',
              'price_import': 'Giá nhập', 'price_export': 'Giá bán', 'description': 'Mô tả'}
    widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
               'category': forms.Select(attrs={'class': 'form-select'}),
               'thumbnail': forms.TextInput(attrs={'class': 'form-control'}),
               'price_import': forms.NumberInput(attrs={'class': 'form-control'}),
               'price_export': forms.NumberInput(attrs={'class': 'form-control'}),
               'description': forms.Textarea(attrs={'class': 'form-control'})}