from django import forms
from .models import Import, ImportDetail

class FormImport(forms.ModelForm):
  class Meta:
    model = Import
    exclude = ('created_by', 'created_date')
    widgets = {'provider': forms.Select(attrs={'class': 'form-select'}), 
               'note': forms.Textarea(attrs={'class': 'form-control'})}
    labels = {'provider': 'Nhà cung cấp', 'note': 'Ghi chú'}
    
class FormImportDetail(forms.ModelForm):
  class Meta:
    model = ImportDetail
    exclude = ('_import', )
    widgets = {'product': forms.Select(attrs={'class': 'form-select'}),
               'quantity': forms.NumberInput(attrs={'class': 'form-control'})}
    labels = {'product': 'Sản phẩm', 'quantity': 'Số lượng'}