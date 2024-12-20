from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from warehouse.models import Export, ExportDetail
from .models import Profile

class FormAddress(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['phone_number','address', 'city', 'province']
    labels = {'phone_number': 'Số điện thoại', 'address': 'Địa chỉ', 'city': 'Thành phố', 'province': 'Tỉnh'}
    widgets = {'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
               'address': forms.TextInput(attrs={'class': 'form-control'}),
               'city': forms.TextInput(attrs={'class': 'form-control'}),
               'province': forms.TextInput(attrs={'class': 'form-control'})}


class FormExport(forms.ModelForm):
  class Meta:
    model = Export
    exclude = ('created_by', 'customer', 'store_note', 'status', 'exported_date')
    widgets = {'customer_note': forms.Textarea(attrs={'class': 'form-control'})}
    labels = {'customer_note': 'Ghi chú'}
    

class FormExportDetail(forms.ModelForm):
  class Meta:
    model = ExportDetail
    exclude = ('export', )
    widgets = {'product': forms.Select(attrs={'class': 'form-select'}),
               'quantity': forms.NumberInput(attrs={'class': 'form-control'})}
    labels = {'product': 'Sản phẩm', 'quantity': 'Số lượng'}
  

class FormUpdateProfile(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ('user', 'permission')
    widgets = {'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
               'address': forms.TextInput(attrs={'class': 'form-control'}),
               'city': forms.TextInput(attrs={'class': 'form-control'}),
               'province': forms.TextInput(attrs={'class': 'form-control'})}
    labels = {'phone_number': 'Số điện thoại', 
              'address': 'Địa chỉ',
              'city': 'Thành phố',
              'province': 'Tỉnh'}
  

class FormUpdateUser(forms.ModelForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name')
    widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
               'last_name': forms.TextInput(attrs={'class': 'form-control'})}
    labels = {'last_name': 'Tên', 
              'first_name': 'Họ',}


class SignInForm(forms.Form):
  username = forms.CharField(label="Tài khoản",min_length=6, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(label="Mật khẩu", min_length=8, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class SignUpForm(UserCreationForm):
  phone_number = forms.CharField(label="Số điện thoại",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
  address = forms.CharField(label="Địa chỉ",max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
  city = forms.CharField(label="Thành phố",max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  province = forms.CharField(label="Tỉnh",max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
  class Meta:
    model = User 
    fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
    widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
               'first_name': forms.TextInput(attrs={'class': 'form-control'}),
               'last_name': forms.TextInput(attrs={'class': 'form-control'})}
    labels = {'username': 'Tài khoản',
              'last_name': 'Tên', 
              'first_name': 'Họ',}

  def __init__(self, *args, **kwargs):
    super(SignUpForm, self).__init__(*args, **kwargs)
    self.fields['username'].help_text = ''
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].label = 'Mật khẩu'
    self.fields['password1'].help_text = ''
    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].label = 'Nhập lại mật khẩu'
    self.fields['password2'].help_text = ''