from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='warehouse'),
  path('nhap-hang/', views.import_product, name='import'),
  path('yeu-cau/', views.require_export, name='require-export'),
  path('san-pham/', views.products, name='products'),
  path('yeu-cau/<int:export_id>/', views.export_detail, name='export-detail')
]