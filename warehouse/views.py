from django.shortcuts import render, redirect
from .forms import FormImport, FormImportDetail
from .models import Import, ImportDetail, Stock, Export
from django.contrib import messages
from datetime import datetime
from store.models import Product
from django.utils import timezone

# Create your views here.
def index(request):
  if request.user.is_authenticated and (request.user.profile.permission == 'Nhân viên' or request.user.profile.permission == 'Quản lý'):
    title = 'Quản lý kho'
    count_export = Export.objects.filter(status='Chờ duyệt').count()
    count_out_of_stock = Stock.objects.filter(out_of_stock=True).count()
    return render(request, 'warehouse/home.html', {'title': title, 'count_export': count_export,
                                                   'count_out_of_stock': count_out_of_stock})
  else:
    return redirect('home')
  
def import_product(request):
  if request.user.is_authenticated and (request.user.profile.permission == 'Nhân viên' or request.user.profile.permission == 'Quản lý'):
    title = 'Nhập hàng'
    form_i = FormImport()
    form_id = FormImportDetail()
    if request.POST:
      form_i = FormImport(request.POST)
      product_ids = request.POST.getlist('product')
      quantities = request.POST.getlist('quantity')
      if form_i.is_valid():
        _import = form_i.save(False)
        _import.created_by = request.user
        _import.save()
        for product_id, quantity in zip(product_ids, quantities):
          ImportDetail.objects.create(_import=_import, product_id=product_id, quantity=quantity)
          stock = Stock.objects.get(product_id=product_id)
          stock.quantity = (stock.quantity or 0) + int(quantity)
          stock.save()
        messages.success(request, 'Nhập hàng thành công')
        return redirect('warehouse')
    return render(request, 'warehouse/import-product.html', {'title': title, 'form_i': form_i, 'form_id': form_id})
  else:
    return redirect('home')

def require_export(request):
  if request.user.is_authenticated and (request.user.profile.permission == 'Nhân viên' or request.user.profile.permission == 'Quản lý'):
    title = 'Yêu cầu xuất kho'
    exports = Export.objects.all().order_by('-required_date')
    status = request.GET.get('status', '')
    start_date = request.GET.get('start-date', '')
    end_date = request.GET.get('end-date', '')
    if status:
      exports = exports.filter(status=status)
    if start_date and end_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      exports = exports.filter(required_date__range=[sd_ed, ed_ed])
    elif start_date:
      sd_ed = timezone.make_aware(datetime.strptime(start_date, "%Y-%m-%d"))
      ed_ed = timezone.make_aware(datetime.now())
      exports = exports.filter(required_date__range=[sd_ed, ed_ed])
    elif end_date:
      ed_ed = timezone.make_aware(datetime.strptime(end_date, "%Y-%m-%d"))
      exports = exports.filter(required_date__range=[exports.earliest('required_date').required_date, ed_ed])
    for export in exports:
      total_amount = sum(ed.total_price for ed in export.exportdetail_set.all())
      export.total_amount = total_amount
    return render(request, 'warehouse/require-export.html', {'title': title, 'exports': exports, 
                                                             'status':status, 'start_date':start_date,
                                                             'end_date': end_date})
  else:
    return redirect('home')
  
def export_detail(request, export_id):
  if request.user.is_authenticated and (request.user.profile.permission == 'Nhân viên' or request.user.profile.permission == 'Quản lý'):
    try:
      export = Export.objects.get(id=export_id)
      title = f'Yêu cầu {export.id}'
      if request.POST:
        action = request.POST.get('action')
        store_note = request.POST.get('store-note')
        if action == 'Không xuất':
          export.status = 'Không xuất'
        if action == 'Đã xuất':
          for ed in export.exportdetail_set.all():
            stock = Stock.objects.get(product=ed.product)
            if stock.quantity < ed.quantity:
              messages.error(request, f"Sản phẩm {ed.product.title} không đủ số lượng trong kho để xuất.")
              return redirect('export-detail', export.id)
            stock.purchased += ed.quantity
            stock.save()
          export.status = 'Đã xuất'
          export.exported_date = datetime.now()
        export.store_note = store_note
        export.created_by = request.user
        export.save()
        messages.success(request, 'Phê duyệt thành công')
        return redirect('require-export')
      return render(request, 'warehouse/export-detail.html', {'title': title, 'export': export})
    except Export.DoesNotExist:
      return redirect('require-export')
  else:
    return redirect('home')
  
def products(request):
  if request.user.is_authenticated and (request.user.profile.permission == 'Nhân viên' or request.user.profile.permission == 'Quản lý'):
    products = Product.objects.all()
    title = 'Tồn kho sản phẩm'
    return render(request, 'warehouse/products.html', {'title':title, 'products': products})
  else:
    return redirect('home')