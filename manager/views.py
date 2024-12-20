from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from warehouse.models import *
from django.utils import timezone
from datetime import datetime
from .forms import FormProduct, FormProvider
from store.forms import SignUpForm
from store.models import Profile

# Create your views here.
def index(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Trang quản lý'
    return render(request, 'manager/home.html', {'title': title})
  else:
    return redirect('home')

def report(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Báo cáo hoạt động'
    list_revenue = []
    list_costly= []
    for stock in Stock.objects.all():
      revenue = stock.purchased * stock.product.price_export
      list_revenue.append(revenue)
      costly = stock.quantity * stock.product.price_import
      list_costly.append(costly)
    count_emp = User.objects.filter(profile__permission='Nhân viên').count
    count_pro = Product.objects.all().count
    count_import = Import.objects.all().count
    count_order = Export.objects.all().count
    count_export = Export.objects.filter(status='Đã xuất').count
    return render(request, 'manager/report.html', {'title': title, 'revenue': sum(list_revenue), 
                                                   'profit': sum(list_revenue) - sum(list_costly),
                                                   'costly': sum(list_costly), 'count_emp': count_emp, 
                                                   'count_pro': count_pro, 'count_import': count_import,
                                                   'count_order': count_order, 'count_export': count_export})
  else:
    return redirect('home')

def users(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Quản lý người dùng'
    users = User.objects.exclude(id=request.user.id)
    permission = request.GET.get('permission', '')
    if permission:
      users = users.filter(profile__permission=permission)
    return render(request, 'manager/users.html', {'title': title, 'users': users, 'permission': permission})
  else:
    return redirect('home')
  
def create_emp(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Thêm nhân viên'
    form = SignUpForm(request.POST or None)
    if request.POST:
      if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user, phone_number = form.cleaned_data['phone_number'],
                                  address=form.cleaned_data['address'],
                                  city=form.cleaned_data['city'],
                                  province=form.cleaned_data['province'],
                                  permission='Nhân viên')
        messages.success(request, 'Tạo nhân viên thành công')
        return redirect('users')
    return render(request, 'store/sign-up.html', {'title':title, 'form': form, 'target': 'Thêm nhân viên'})
  else:
    return redirect('home')
  
def user_detail(request, user_id):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    try:
      user = User.objects.get(id=user_id)
      title = user.username
      if request.POST:
        action = request.POST.get('action')
        if action == 'delete':
          user.delete()
          messages.success(request, 'Đã xóa người dùng')
        if action == 'permission':
          if user.profile.permission == 'Nhân viên':
            user.profile.permission = 'Khách hàng'
          elif user.profile.permission == 'Khách hàng':
            user.profile.permission = 'Nhân viên'
          user.profile.save()
          messages.success(request, 'Đã thay đổi quyền người dùng')
        return redirect('users')
      return render(request, 'manager/user-detail.html', {'title': title, 'user': user})
    except User.DoesNotExist:
      return redirect('users')
  else:
    return redirect('home')
  
def import_product(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Quản lý nhập hàng'
    providers = Provider.objects.all()
    imports = Import.objects.all().order_by('-created_date')
    req_provider = request.GET.get('provider', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if req_provider:
      imports = imports.filter(provider__name=req_provider)
    if start_date and end_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      imports = imports.filter(created_date__range=[sd_ed, ed_ed])
    elif start_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.now())
      imports = imports.filter(created_date__range=[sd_ed, ed_ed])
    elif end_date:
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      imports = imports.filter(created_date__range=[imports.earliest('created_date').created_date, ed_ed])
    for imp in imports:
      total_amount = sum(imd.total_price for imd in imp.importdetail_set.all())
      imp.total_amount = total_amount
    return render(request, 'manager/import-product.html', {'title': title, 'imports': imports, 
                                                           'providers': providers, 'req_provider': req_provider,
                                                           'start_date': start_date, 'end_date':end_date})
  else:
    return redirect('home')
  
def import_detail(request, import_id):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    try:
      _import = Import.objects.get(id=import_id)
      title = f'Chi tiết nhập hàng {import_id}'
      return render(request, 'manager/import-detail.html', {'title': title, 'import': _import})
    except Import.DoesNotExist:
      return redirect('import-product')
  else:
    return redirect('home')
  
def products(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    products = Product.objects.all()
    title = 'Quản lý sản phẩm'
    return render(request, 'manager/products.html', {'title':title, 'products': products})
  else:
    return redirect('home')
  
def product_detail(request, pro_id):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    try:
      product = Product.objects.get(id=pro_id)
      title = product.title
      if request.POST:
        product.delete()
        messages.success(request, 'Đã xóa sản phẩm')
        return redirect('manage-product')
      return render(request, 'manager/product-detail.html', {'title':title, 'product': product})
    except Product.DoesNotExist:
      return redirect('manage')
  else:
    return redirect('home')
  
def product_cu(request, pro_id=None):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    if pro_id:
      try:
        product = Product.objects.get(id=pro_id)
        title = f'Sửa sản phẩm {product.title}'
        form = FormProduct(instance=product)
      except Product.DoesNotExist:
        return redirect('manage')
    else:
      product = None
      title = 'Thêm mới sản phẩm'
      form = FormProduct()
    if request.POST:
      form = FormProduct(request.POST, instance=product)
      if form.is_valid():
          product = form.save(False)
          product.slug = slugify(product.title)
          product.save()
          message = 'Sửa sản phẩm thành công' if pro_id else 'Thêm sản phẩm thành công'
          messages.success(request, message)
          return redirect('manage-product')
    return render(request, 'manager/product-cu.html', {'title':title, 'form': form})
  else:
    return redirect('home')
  
def providers(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Danh sách nhà cung cấp'
    providers = Provider.objects.all()
    if request.POST:
      provider_id = request.POST.get('delete')
      Provider.objects.get(id=provider_id).delete()
      messages.success(request, 'Xóa thành công nhà cung cấp')
    return render(request, 'manager/providers.html', {'title': title, 'providers': providers})
  else:
    return redirect('home')

def create_provider(request):
  if request.user.is_authenticated and request.user.profile.permission == 'Quản lý':
    title = 'Tạo nhà cung cấp'
    form = FormProvider()
    if request.POST:
      form = FormProvider(request.POST)
      if form.is_valid():
        form.save()
        messages.success(request, 'Đã thêm nhà cung ứng')
        return redirect('providers')
    return render(request, 'manager/create-provider.html', {'title': title, 'form': form})
  else:
    return redirect('home')