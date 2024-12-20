from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from .forms import *
from .models import Profile, Product, Category
from django.contrib import messages
from warehouse.models import Export, ExportDetail

# Create your views here.
def index(request):
  title = 'Web Vật Tư'
  categories = Category.objects.all()
  return render(request, 'store/home.html', {'title': title, 'categories': categories})

def sign_up(request):
  title = 'Đăng ký'
  form = SignUpForm()
  if request.POST:
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      Profile.objects.create(user=user, phone_number = form.cleaned_data['phone_number'],
                                       address=form.cleaned_data['address'],
                                       city=form.cleaned_data['city'],
                                       province=form.cleaned_data['province'])
      return redirect('sign-in')
  return render(request, 'store/sign-up.html', {'title': title, 'form': form})

def sign_in(request):
  title = 'Đăng nhập'
  form = SignInForm()
  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user: 
      auth.login(request, user)
      return redirect('home')
    else:
      messages.warning(request, 'Tài khoản hoặc mật khẩu không đúng')
  return render(request, 'store/sign-in.html', {'title': title, 'form': form})

def logout(request):
  auth.logout(request)
  return redirect('home')

def profile(request):
  if request.user.is_authenticated:
    title = f'Hồ sơ {request.user.first_name} {request.user.last_name}'
    return render(request, 'store/profile.html', {'title': title})
  else:
    return redirect('sign-in')
  
def update_profile(request, username):
  if request.user.username == username:
    title = f'Sửa hồ sơ {request.user.first_name} {request.user.last_name}'
    form_u = FormUpdateUser(instance=request.user)
    form_p = FormUpdateProfile(instance=request.user.profile)
    if request.POST:
      form_u = FormUpdateUser(request.POST, instance=request.user)
      form_p = FormUpdateProfile(request.POST, instance=request.user.profile)
      if form_p.is_valid() and form_u.is_valid():
        form_u.save()
        form_p.save()
        messages.success(request, 'Đã sửa thông tin')
        return redirect('profile')
    return render(request, 'store/update-profile.html', {'title': title, 'form_p': form_p, 'form_u': form_u})
  else:
    return redirect('home')

def category(request, cat_slug):
  try:
    category = Category.objects.get(slug=cat_slug)
    title = category.name
    products = Product.objects.filter(category = category)
    return render(request, 'store/category.html', {'title': title, 'products': products})
  except Category.DoesNotExist:
    return redirect('home')


def product(request, cat_slug, pro_slug):
  try:
    product = Product.objects.get(category__slug=cat_slug, slug=pro_slug)
    title = product.title
    return render(request, 'store/product.html', {'title': title, 'product': product})
  except Product.DoesNotExist:
    return redirect('home')
  
def order(request):
  if request.user.is_authenticated:
    title = 'Đặt hàng'
    form_a = FormAddress(request.POST or None, instance=request.user.profile)
    form_e = FormExport(request.POST or None)
    form_ed = FormExportDetail()
    if request.POST and request.user.profile.permission == 'Khách hàng':
      product_ids = request.POST.getlist('product')
      quantities = request.POST.getlist('quantity')
      if form_e.is_valid() and form_a.is_valid():
        form_a.save()
        export = form_e.save(False)
        export.customer = request.user
        export.save()
        for product_id, quantity in zip(product_ids, quantities):
          ExportDetail.objects.create(export=export, product_id=product_id, quantity=quantity)
        messages.success(request, 'Đã đặt hàng')
        return redirect('home')
    elif request.POST and request.user.profile.permission == 'Nhân viên':
      messages.warning(request, 'Bạn không thể đặt hàng')  
    return render(request, 'store/order.html', {'title':title, 'form_a': form_a,'form_e': form_e, 'form_ed': form_ed})
  else:
    return redirect('sign-in')
  
def my_order(request):
  if request.user.is_authenticated:
    title = 'Đơn hàng của tôi'
    exports = Export.objects.filter(customer=request.user)
    for export in exports:
      total_amount = sum(ed.total_price for ed in export.exportdetail_set.all())
      export.total_amount = total_amount
    return render(request, 'store/my-order.html', {'title': title, 'exports': exports})
  else:
    return redirect('home')
  
def order_detail(request, export_id):
  try:
    export = Export.objects.get(customer=request.user, id=export_id)
    title = f'Đơn hàng {export.id}'
    return render(request, 'store/order-detail.html', {'title': title, 'export':export})
  except Export.DoesNotExist:
    return redirect('home')